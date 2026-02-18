import pytest
from django.utils import timezone

pytestmark = pytest.mark.django_db


def test_submit_telemetry(api_client, device):
    """
    Feature: Telemetry
    Scenario: Submit telemetry data
    """
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
    assert response.data["device_id"] == device["id"]


def test_get_telemetry_for_device(api_client, device):
    """
    Feature: Telemetry
    Scenario: Get telemetry for a device
    """
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
    assert len(response.data) >= 1


def test_get_telemetry_within_date_range(api_client, device):
    """
    Feature: Business Logic
    Scenario: Get telemetry data within date range
    """
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
        f"/api/devices/{device['id']}/telemetry/"
        f"?start_date={today}&end_date={today}"
    )

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) >= 1


def test_last_seen_updated_after_telemetry_submission(api_client, device):
    """
    Feature: Telemetry
    Scenario: Update last_seen when telemetry is submitted

    Notes:
    - last_seen is updated via signal
    - value may come from Redis cache, not DB
    - test verifies observable behavior, not implementation
    """

    # Given: a device exists and has an initial last_seen
    initial_response = api_client.get(
        f"/api/devices/{device['id']}/"
    )
    initial_last_seen = initial_response.data.get("last_seen")

    # When: telemetry is submitted
    telemetry_response = api_client.post(
        "/api/telemetry/",
        {
            "device_id": device["id"],
            "temperature": 26.0,
            "humidity": 65,
        },
        format="json"
    )

    assert telemetry_response.status_code == 201

    # Then: device last_seen should be updated (regardless of source)
    updated_response = api_client.get(
        f"/api/devices/{device['id']}/"
    )

    updated_last_seen = updated_response.data.get("last_seen")

    assert updated_last_seen is not None
    assert updated_last_seen != initial_last_seen