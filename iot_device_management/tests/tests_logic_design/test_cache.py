import pytest
from telemetry.models import TelemetryData
from django.utils.timezone import now
from django.core.cache import cache
from devices.serializers import DeviceSerializer
from django.utils.dateparse import parse_datetime
from datetime import datetime

pytestmark = pytest.mark.django_db


def test_last_seen_cached_after_telemetry_created(device):
    """
    When telemetry is created,
    device last_seen should be written to cache
    """

    cache_key = f"device:last_seen:{device.id}"
    cache.delete(cache_key)

    # When
    TelemetryData.objects.create(
        device=device,
        metric_name="temperature",
        metric_value=60,
        timestamp=now(),
    )

    # Then
    cached_value = cache.get(cache_key)

    assert cached_value is not None


def test_device_serializer_reads_last_seen_from_cache(device):
    """
    Serializer should prefer cache over DB for last_seen
    """

    cached_time = now()
    cache_key = f"device:last_seen:{device.id}"

    cache.set(cache_key, cached_time)

    serializer = DeviceSerializer(device)
    data = serializer.data
    value = data["last_seen"]
    if isinstance(value, datetime):
        assert value == cached_time
    else:
        assert parse_datetime(value) == cached_time


def test_device_serializer_fallbacks_to_db_last_seen(device):
    """
    If cache is empty, serializer should return DB last_seen
    """

    cache_key = f"device:last_seen:{device.id}"
    cache.delete(cache_key)

    device.last_seen = now()
    device.save(update_fields=["last_seen"])

    serializer = DeviceSerializer(device)
    data = serializer.data

    assert data["last_seen"] is not None


def test_telemetry_aggregation_is_cached(api_client, device):
    """
    Aggregation result should be cached
    """

    TelemetryData.objects.create(
        device=device,
        metric_name="temperature",
        metric_value=30,
        timestamp=now(),
    )
    TelemetryData.objects.create(
        device=device,
        metric_name="temperature",
        metric_value=60,
        timestamp=now(),
    )

    cache_key = f"telemetry:stats:{device.id}:None:None"
    cache.delete(cache_key)

    # First call → compute + cache
    response1 = api_client.get(
        f"/api/devices/{device.id}/telemetry/stats/"
    )
    assert response1.status_code == 200

    cached_value = cache.get(cache_key)
    assert cached_value is not None

    # Second call → should hit cache
    response2 = api_client.get(
        f"/api/devices/{device.id}/telemetry/stats/"
    )

    assert response1.json() == response2.json()
