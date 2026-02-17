Feature: Business Logic for Devices and Telemetry
  As a system
  I want to enforce business rules
  So that data is consistent and reliable

  Background:
    Given the API service is running

  # --------------------
  # Device Filtering
  # --------------------
  Scenario: Filter devices by customer_id
    Given multiple devices exist for different customers
    When I send a GET request to "/api/devices/?customer_id=10"
    Then the response status code should be 200
    And only devices for customer_id "10" should be returned

  Scenario: Filter devices by device_type
    Given multiple devices with different types exist
    When I send a GET request to "/api/devices/?device_type=sensor"
    Then the response should contain only devices of type "sensor"

  Scenario: Filter devices by active status
    Given active and inactive devices exist
    When I send a GET request to "/api/devices/?is_active=true"
    Then the response should contain only active devices

  # --------------------
  # Last Seen Update
  # --------------------
  Scenario: Update last_seen when telemetry is submitted
    Given a device with id "1" exists
    And the device has an old last_seen value
    When telemetry data is submitted for device "1"
    Then the device last_seen field should be updated to the current time

  # --------------------
  # Telemetry Query
  # --------------------
  Scenario: Get telemetry data within a date range
    Given a device with id "1" has telemetry data
    When I send a GET request to "/api/devices/1/telemetry/?start_date=2024-01-01&end_date=2024-01-31"
    Then the response status code should be 200
    And only telemetry data within the date range should be returned

  # --------------------
  # Validation
  # --------------------
  Scenario: Reject invalid email format when creating customer
    Given I have customer data with an invalid email
    When I send a POST request to "/api/customers/"
    Then the response status code should be 400
    And the response should contain a validation error

  Scenario: Reject invalid device type
    Given I have device data with an invalid device_type
    When I send a POST request to "/api/devices/"
    Then the response status code should be 400
    And the response should contain a validation error
