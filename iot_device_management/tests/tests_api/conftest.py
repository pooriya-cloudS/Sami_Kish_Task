import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


@pytest.fixture(scope="function")
def api_client():
    """
    DRF API client.
    New instance per test to guarantee isolation.
    """
    client = APIClient()
    return client


@pytest.fixture
def authenticated_user(db):
    """
    Create an authenticated user for testing
    """
    user = User.objects.create_user(
        email="testuser@example.com", name="Test User", password="testpass123"
    )
    return user


@pytest.fixture
def authenticated_api_client(authenticated_user):
    """
    API client with JWT authentication
    """
    client = APIClient()
    refresh = RefreshToken.for_user(authenticated_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
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
def customer(authenticated_api_client):
    response = authenticated_api_client.post(
        "/api/users/",
        {
            "name": "Test Customer",
            "email": "testcustomer@example.com",
        },
        format="json",
    )
    return response.data


@pytest.fixture
def device_payload(customer):
    return {
        "name": "Test Device",
        "serial_number": "DEVICE-001-TEST",
        "device_type": "sensor",
        "customer": customer["id"],
        "is_active": True,
    }


@pytest.fixture
def device(authenticated_api_client, device_payload):
    response = authenticated_api_client.post(
        "/api/devices/", device_payload, format="json"
    )
    return response.data
