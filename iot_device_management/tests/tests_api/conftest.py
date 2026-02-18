import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def api_client():
    """
    DRF API client.
    New instance per test to guarantee isolation.
    """
    client = APIClient()
    return client



@pytest.fixture
def customer_payload():
    """
    Valid customer payload
    """
    return {
        "name": "Test Customer",
        "email": "test@example.com",
    }

@pytest.fixture
def customer(api_client):
    response = api_client.post(
        "/api/customers/",
        {
            "name": "Test Customer",
            "email": "test@example.com",
        },
        format="json",
    )
    return response.data


@pytest.fixture
def device_payload(customer):
    return {
        "name": "Test Device",
        "device_type": "sensor",
        "customer_id": customer["id"],
        "is_active": True,
    }

@pytest.fixture
def device(api_client, device_payload):
    response = api_client.post(
        "/api/devices/",
        device_payload,
        format="json"
    )
    return response.data