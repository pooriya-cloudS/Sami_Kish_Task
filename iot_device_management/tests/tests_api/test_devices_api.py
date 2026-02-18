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


def test_create_device(api_client, device_payload):
    """
    Feature: Devices
    Scenario: Register a new device
    """
    response = api_client.post(
        "/api/devices/",
        device_payload,
        format="json"
    )

    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["device_type"] == device_payload["device_type"]


def test_get_device_by_id(api_client, device_payload):
    """
    Feature: Devices
    Scenario: Retrieve device details by id
    """
    create = api_client.post(
        "/api/devices/",
        device_payload,
        format="json"
    )
    device_id = create.data["id"]

    response = api_client.get(f"/api/devices/{device_id}/")

    assert response.status_code == 200
    assert response.data["id"] == device_id


def test_update_device(api_client, device_payload):
    """
    Feature: Devices
    Scenario: Update device information
    """
    create = api_client.post(
        "/api/devices/",
        device_payload,
        format="json"
    )
    device_id = create.data["id"]

    response = api_client.patch(
        f"/api/devices/{device_id}/",
        {"is_active": False},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["is_active"] is False


def test_delete_device(api_client, device_payload):
    """
    Feature: Devices
    Scenario: Delete a device
    """
    create = api_client.post(
        "/api/devices/",
        device_payload,
        format="json"
    )
    device_id = create.data["id"]

    response = api_client.delete(f"/api/devices/{device_id}/")

    assert response.status_code == 204


def test_filter_devices_by_customer(api_client, device_payload, customer):
    """
    Feature: Devices
    Scenario: Filter devices by customer_id
    """
    api_client.post("/api/devices/", device_payload, format="json")

    response = api_client.get(
        f"/api/devices/?customer_id={customer['id']}"
    )

    assert response.status_code == 200
    assert len(response.data) >= 1
    for device in response.data:
        assert device["customer_id"] == customer["id"]


def test_filter_devices_by_active_status(api_client, device_payload):
    """
    Feature: Devices
    Scenario: Filter devices by active status
    """
    payload = device_payload | {"is_active": False}

    api_client.post("/api/devices/", payload, format="json")

    response = api_client.get("/api/devices/?is_active=false")

    assert response.status_code == 200
    for device in response.data:
        assert device["is_active"] is False


def test_filter_devices_by_device_type(api_client, device_payload):
    """
    Feature: Devices
    Scenario: Filter devices by device_type
    """
    api_client.post(
        "/api/devices/",
        device_payload | {"device_type": "sensor"},
        format="json"
    )

    api_client.post(
        "/api/devices/",
        device_payload | {"device_type": "gateway"},
        format="json"
    )

    response = api_client.get("/api/devices/?device_type=sensor")

    assert response.status_code == 200
    for device in response.data:
        assert device["device_type"] == "sensor"
