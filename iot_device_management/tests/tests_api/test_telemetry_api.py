import pytest
from django.utils import timezone

pytestmark = pytest.mark.django_db


def test_submit_telemetry(authenticated_api_client, device):
    """
    Feature: Telemetry
    Scenario: Submit telemetry data
    """
    response = authenticated_api_client.post(
        "/api/telemetry/",
        {
            "device": device["id"],
            "metric_value": 22,
            "metric_name": "temperature",
            "humidity": 55,
        },
        format="json"
    )
    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["device"] == device["id"]


def test_get_telemetry_for_device(authenticated_api_client, device):
    """
    Feature: Telemetry
    Scenario: Get telemetry for a device
    """
    authenticated_api_client.post(
        "/api/telemetry/",
        {
            "device": device["id"],
            "metric_value": 22,
            "metric_name": "temperature",
            "humidity": 60,
        },
        format="json"
    )

    response = authenticated_api_client.get(
        f"/api/devices/{device['id']}/telemetry/"
    )

    assert response.status_code == 200
    results = response.data.get("results", response.data)
    assert isinstance(results, list)
    assert len(results) >= 1


def test_get_telemetry_within_date_range(authenticated_api_client, device):
    """
    Feature: Business Logic
    Scenario: Get telemetry data within date range
    """
    # ابتدا telemetry را ثبت کنید
    authenticated_api_client.post(
        "/api/telemetry/",
        {
            "device": device["id"],
            "metric_value": 22,
            "metric_name": "temperature",
            "timestamp": timezone.now().isoformat(),
        },
        format="json"
    )

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999).strftime("%Y-%m-%d %H:%M:%S")

    response = authenticated_api_client.get(
        f"/api/devices/{device['id']}/telemetry/"
        f"?start_date={today_start}&end_date={today_end}"
    )

    assert response.status_code == 200
    results = response.data.get("results", response.data)
    assert isinstance(results, list)
    assert len(results) >= 1


def test_last_seen_updated_after_telemetry_submission(authenticated_api_client, device):
    """
    Feature: Telemetry
    Scenario: Update last_seen when telemetry is submitted

    Notes:
    - last_seen is updated via signal
    - value may come from Redis cache, not DB
    - test verifies observable behavior, not implementation
    """

    # Given: a device exists and has an initial last_seen
    initial_response = authenticated_api_client.get(
        f"/api/devices/{device['id']}/"
    )
    initial_last_seen = initial_response.data.get("last_seen")

    # When: telemetry is submitted
    telemetry_response = authenticated_api_client.post(
        "/api/telemetry/",
        {
            "device": device["id"],
            "metric_value": 22,
            "metric_name": "temperature",
            "humidity": 65,
        },
        format="json"
    )

    assert telemetry_response.status_code == 201

    # Then: device last_seen should be updated (regardless of source)
    updated_response = authenticated_api_client.get(
        f"/api/devices/{device['id']}/"
    )

    updated_last_seen = updated_response.data.get("last_seen")

    assert updated_last_seen is not None
    assert updated_last_seen != initial_last_seen