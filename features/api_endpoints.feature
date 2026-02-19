Feature: REST API Endpoints for Customers, Devices, and Telemetry
  As an API consumer
  I want to manage customers, devices, and telemetry data
  So that I can build a device monitoring platform

  Background:
    Given the API service is running

  # --------------------
  # Customers
  # --------------------
  Scenario: List all customers
    When I send a GET request to "/api/customers/"
    Then the response status code should be 200
    And the response should contain a list of customers

  Scenario: Create a new customer
    Given I have valid customer data
    When I send a POST request to "/api/customers/"
    Then the response status code should be 201
    And the customer should be created successfully

  # --------------------
  # Devices
  # --------------------
  Scenario: List all devices
    When I send a GET request to "/api/devices/"
    Then the response status code should be 200
    And the response should contain a list of devices

  Scenario: Register a new device
    Given I have valid device data
    When I send a POST request to "/api/devices/"
    Then the response status code should be 201
    And the device should be registered successfully

  Scenario: Retrieve device details by id
    Given a device with id "1" exists
    When I send a GET request to "/api/devices/1/"
    Then the response status code should be 200
    And the response should contain device details

  Scenario: Update device information
    Given a device with id "1" exists
    And I have updated device data
    When I send a PATCH request to "/api/devices/1/"
    Then the response status code should be 200
    And the device information should be updated

  Scenario: Delete a device
    Given a device with id "1" exists
    When I send a DELETE request to "/api/devices/1/"
    Then the response status code should be 204
    And the device should be deleted

  # --------------------
  # Telemetry
  # --------------------
  Scenario: Submit telemetry data for a device
    Given a device with id "1" exists
    And I have valid telemetry data
    When I send a POST request to "/api/telemetry/"
    Then the response status code should be 201
    And the telemetry data should be stored

  Scenario: Get telemetry data for a device
    Given a device with id "1" exists
    When I send a GET request to "/api/devices/1/telemetry/"
    Then the response status code should be 200
    And the response should contain telemetry records
