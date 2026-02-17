import pytest

pytestmark = pytest.mark.django_db


def test_submit_telemetry(api_client):
    """
    Feature: Telemetry
    Scenario: Submit telemetry data
    """
    device = api_client.post(
        "/api/devices/",
        {
            "name": "Telemetry Device",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    ).data

    response = api_client.post(
        "/api/telemetry/",
        {
            "device_id": device["id"],
            "temperature": 22.5,
            "humidity": 55,
        },
        format="json"
    )

    assert response.status_code == 201
    assert "id" in response.data

def test_get_telemetry_for_device(api_client):
    """
    Feature: Telemetry
    Scenario: Get telemetry for a device
    """
    device = api_client.post(
        "/api/devices/",
        {
            "name": "Device A",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    ).data

    api_client.post(
        "/api/telemetry/",
        {
            "device_id": device["id"],
            "temperature": 25,
            "humidity": 60,
        },
        format="json"
    )

    response = api_client.get(
        f"/api/devices/{device['id']}/telemetry/"
    )

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) > 0

from django.utils import timezone


def test_get_telemetry_within_date_range(api_client):
    """
    Feature: Business Logic
    Scenario: Get telemetry data within date range
    """
    device = api_client.post(
        "/api/devices/",
        {
            "name": "Range Device",
            "device_type": "sensor",
            "customer_id": 1,
            "is_active": True,
        },
        format="json"
    ).data

    api_client.post(
        "/api/telemetry/",
        {
            "device_id": device["id"],
            "temperature": 20,
            "humidity": 50,
        },
        format="json"
    )

    today = timezone.now().date().isoformat()

    response = api_client.get(
        f"/api/devices/{device['id']}/telemetry/?start_date={today}&end_date={today}"
    )

    assert response.status_code == 200
