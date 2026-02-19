import pytest
from django.core.cache import cache
from devices.models import Device
from users.models import User
from django.utils.timezone import now
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test123@example.com",
        password="testpass123",
    )


@pytest.fixture
def api_client(db, user):
    """
    Authenticated API client using JWT
    """
    client = APIClient()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    return client


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def customer(db):
    return User.objects.create(
        name="Test Customer",
        email="test@example.com",
    )


@pytest.fixture
def device(db, customer):
    return Device.objects.create(
        customer=customer,
        name="Test Device",
        device_type="sensor",
        is_active=True,
        last_seen=now(),
    )
