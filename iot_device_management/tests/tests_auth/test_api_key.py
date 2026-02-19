import pytest
import secrets
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from authentication.models import APIKey
from devices.models import Device


@pytest.fixture
def api_client():
    return APIClient()


User = get_user_model()


@pytest.fixture
def api_key(db):
    return APIKey.objects.create(
        name="test-key",
        key=secrets.token_hex(32),
        is_active=True,
    )


@pytest.fixture
def customer(db):
    return User.objects.create_user(email="testcustomer@gmail.com", password="password123")


@pytest.fixture
def device(db, customer):
    return Device.objects.create(name="test-device", customer=customer)


def test_submit_telemetry_with_api_key(api_client, api_key, device):
    response = api_client.post(
        "/api/telemetry/",
        {
            "device": device.id,
            "metric_name": "temperature",
            "metric_value": 25,
        },
        HTTP_X_API_KEY=api_key.key,
        format="json",
    )

    assert response.status_code == 201
