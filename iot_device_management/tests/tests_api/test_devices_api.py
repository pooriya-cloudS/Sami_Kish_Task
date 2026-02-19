import pytest

pytestmark = pytest.mark.django_db


def test_list_devices(authenticated_api_client):
    """
    Feature: Devices
    Scenario: List all devices
    """
    response = authenticated_api_client.get("/api/devices/")
    results = response.data.pop("results")

    assert response.status_code == 200
    assert isinstance(results, list)


def test_create_device(authenticated_api_client, device_payload):
    """
    Feature: Devices
    Scenario: Register a new device
    """
    response = authenticated_api_client.post(
        "/api/devices/", device_payload, format="json"
    )
    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["device_type"] == device_payload["device_type"]


def test_get_device_by_id(authenticated_api_client, device_payload):
    """
    Feature: Devices
    Scenario: Retrieve device details by id
    """
    create = authenticated_api_client.post(
        "/api/devices/", device_payload, format="json"
    )
    device_id = create.data["id"]

    response = authenticated_api_client.get(f"/api/devices/{device_id}/")

    assert response.status_code == 200
    assert response.data["id"] == device_id


def test_update_device(authenticated_api_client, device_payload):
    """
    Feature: Devices
    Scenario: Update device information
    """
    create = authenticated_api_client.post(
        "/api/devices/", device_payload, format="json"
    )
    device_id = create.data["id"]

    response = authenticated_api_client.patch(
        f"/api/devices/{device_id}/", {"is_active": False}, format="json"
    )

    assert response.status_code == 200
    assert response.data["is_active"] is False


def test_delete_device(authenticated_api_client, device_payload):
    """
    Feature: Devices
    Scenario: Delete a device
    """
    create = authenticated_api_client.post(
        "/api/devices/", device_payload, format="json"
    )
    device_id = create.data["id"]

    response = authenticated_api_client.delete(f"/api/devices/{device_id}/")

    assert response.status_code == 204


def test_filter_devices_by_customer(authenticated_api_client, device_payload, customer):
    """
    Feature: Devices
    Scenario: Filter devices by customer_id
    """
    authenticated_api_client.post("/api/devices/", device_payload, format="json")

    response = authenticated_api_client.get(
        f"/api/devices/?customer_id={customer['id']}"
    )
    assert response.status_code == 200
    results = response.data.get("results", response.data)
    assert len(results) >= 1
    for device in results:
        assert device["customer"] == customer["id"]


def test_filter_devices_by_active_status(authenticated_api_client, device_payload):
    """
    Feature: Devices
    Scenario: Filter devices by active status
    """
    payload = device_payload | {"is_active": False}

    authenticated_api_client.post("/api/devices/", payload, format="json")

    response = authenticated_api_client.get("/api/devices/?is_active=false")

    assert response.status_code == 200
    results = response.data.get("results", response.data)
    for device in results:
        assert device["is_active"] is False


def test_filter_devices_by_device_type(authenticated_api_client, device_payload):
    """
    Feature: Devices
    Scenario: Filter devices by device_type
    """
    authenticated_api_client.post(
        "/api/devices/", device_payload | {"device_type": "sensor"}, format="json"
    )

    authenticated_api_client.post(
        "/api/devices/", device_payload | {"device_type": "gateway"}, format="json"
    )

    response = authenticated_api_client.get("/api/devices/?device_type=sensor")

    assert response.status_code == 200
    results = response.data.get("results", response.data)
    for device in results:
        assert device["device_type"] == "sensor"
