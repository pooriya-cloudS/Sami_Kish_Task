import pytest

pytestmark = pytest.mark.django_db


def test_list_devices(api_client):
    """
    Feature: Devices
    Scenario: List all devices
    """
    response = api_client.get("/api/devices/")

    assert response.status_code == 200
    assert isinstance(response.data, list)


def test_create_device(api_client):
    """
    Feature: Devices
    Scenario: Register a new device
    """
    payload = {
        "name": "Temperature Sensor",
        "device_type": "sensor",
        "customer_id": 1,
        "is_active": True,
    }

    response = api_client.post(
        "/api/devices/",
        payload,
        format="json"
    )

    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["device_type"] == payload["device_type"]


def test_get_device_by_id(api_client):
    """
    Feature: Devices
    Scenario: Retrieve device details by id
    """
    create_response = api_client.post(
        "/api/devices/",
        {
            "name": "Pressure Sensor",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    )

    device_id = create_response.data["id"]

    response = api_client.get(f"/api/devices/{device_id}/")

    assert response.status_code == 200
    assert response.data["id"] == device_id


def test_update_device(api_client):
    """
    Feature: Devices
    Scenario: Update device information
    """
    create_response = api_client.post(
        "/api/devices/",
        {
            "name": "Old Device",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    )

    device_id = create_response.data["id"]

    response = api_client.patch(
        f"/api/devices/{device_id}/",
        {"is_active": False},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["is_active"] is False


def test_delete_device(api_client):
    """
    Feature: Devices
    Scenario: Delete a device
    """
    create_response = api_client.post(
        "/api/devices/",
        {
            "name": "To Be Deleted",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    )

    device_id = create_response.data["id"]

    response = api_client.delete(f"/api/devices/{device_id}/")

    assert response.status_code == 204


def test_filter_devices_by_customer(api_client):
    """
    Feature: Devices
    Scenario: Filter devices by customer_id
    """
    api_client.post(
        "/api/devices/",
        {
            "name": "Device A",
            "device_type": "sensor",
            "customer_id": 10,
            "is_active": True,
        },
        format="json"
    )

    response = api_client.get("/api/devices/?customer_id=10")

    assert response.status_code == 200
    for device in response.data:
        assert device["customer_id"] == 10


def test_filter_devices_by_active_status(api_client):
    """
    Feature: Devices
    Scenario: Filter devices by active status
    """
    api_client.post(
        "/api/devices/",
        {
            "name": "Inactive Device",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": False,
        },
        format="json"
    )

    response = api_client.get("/api/devices/?is_active=false")

    assert response.status_code == 200
    for device in response.data:
        assert device["is_active"] is False

def test_filter_devices_by_device_type(api_client):
    """
    Feature: Devices
    Scenario: Filter devices by device_type
    """
    # Create devices with different types
    api_client.post(
        "/api/devices/",
        {
            "name": "Temp Sensor",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    )

    api_client.post(
        "/api/devices/",
        {
            "name": "Gateway Device",
            "device_type": "gateway",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    )

    response = api_client.get("/api/devices/?device_type=sensor")

    assert response.status_code == 200
    for device in response.data:
        assert device["device_type"] == "sensor"



def test_update_last_seen_when_telemetry_submitted(api_client):
    """
    Feature: Telemetry
    Scenario: Update last_seen when telemetry is submitted
    """

    # Create device
    create_response = api_client.post(
        "/api/devices/",
        {
            "name": "Telemetry Device",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    )

    device_id = create_response.data["id"]

    # Get initial device state
    initial_response = api_client.get(f"/api/devices/{device_id}/")
    initial_last_seen = initial_response.data.get("last_seen")

    # Submit telemetry
    telemetry_response = api_client.post(
        "/api/telemetry/",
        {
            "device_id": device_id,
            "temperature": 25.5,
            "humidity": 60,
        },
        format="json"
    )

    assert telemetry_response.status_code == 201

    # Fetch device again
    updated_response = api_client.get(f"/api/devices/{device_id}/")

    assert updated_response.status_code == 200
    assert updated_response.data["last_seen"] is not None
    assert updated_response.data["last_seen"] != initial_last_seen
