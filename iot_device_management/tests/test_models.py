import pytest
from django.utils import timezone
from users.models import User
from devices.models import Device
from telemetry.models import TelemetryData


# -------------------------
# User model tests
# -------------------------

@pytest.mark.django_db
def test_create_user():
    """
    Test creating a new User instance and verifying its fields.
    """
    user = User.objects.create_user(
        email="user@example.com",
        name="Test User",
        password="password123"
    )

    assert user.email == "user@example.com"
    assert user.name == "Test User"
    assert user.is_active is True
    assert user.is_admin is False
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.expire_at is None
    assert user.update_at is not None
    assert user.created_at is not None


@pytest.mark.django_db
def test_user_str_and_full_name():
    """
    Test __str__ and get_full_name methods of User model.
    """
    user = User.objects.create_user(email="user2@example.com", name="Full Name", password="password123")

    # __str__ should return the email
    assert str(user) == "user2@example.com"

    # get_full_name should return the user's name
    assert user.get_full_name() == "Full Name"


@pytest.mark.django_db
def test_user_permissions():
    """
    Test has_perm and has_module_perms methods of User model.
    """
    user = User.objects.create_user(email="admin@example.com", name="Admin User", password="password123")

    # By default, is_admin is False, so has_perm should return False
    assert user.has_perm("any_perm") is False
    assert user.has_module_perms("any_module") is True

    # Set is_admin to True
    user.is_admin = True
    user.save()

    assert user.has_perm("any_perm") is True


# -------------------------
# Device and TelemetryData tests
# -------------------------

@pytest.mark.django_db
def test_create_device():
    """
    Test creating a Device instance and verifying its fields.
    """
    # Create a user to be the customer
    user = User.objects.create_user(email="test@example.com", name="Test User", password="password123")

    device = Device.objects.create(
        serial_number="SN12345",
        name="Temperature Sensor",
        device_type=Device.SENSOR,
        customer=user,
        is_active=True
    )

    assert device.serial_number == "SN12345"
    assert device.name == "Temperature Sensor"
    assert device.device_type == Device.SENSOR
    assert device.customer == user
    assert device.is_active is True
    assert device.last_seen is None


@pytest.mark.django_db
def test_create_telemetry_data():
    """
    Test creating TelemetryData and verifying its fields and timestamp.
    """
    user = User.objects.create_user(email="test2@example.com", name="User 2", password="password123")
    device = Device.objects.create(
        serial_number="SN67890",
        name="Humidity Sensor",
        device_type=Device.SENSOR,
        customer=user
    )

    telemetry = TelemetryData.objects.create(
        device=device,
        metric_name="humidity",
        metric_value=45.5
    )

    assert telemetry.device == device
    assert telemetry.metric_name == "humidity"
    assert telemetry.metric_value == 45.5
    assert telemetry.timestamp is not None  # auto_now_add should work


@pytest.mark.django_db
def test_device_telemetry_relationship():
    """
    Test the reverse relationship between Device and TelemetryData.
    """
    user = User.objects.create_user(email="rel@example.com", name="Rel User", password="password123")
    device = Device.objects.create(
        serial_number="SNREL001",
        name="Gateway 1",
        device_type=Device.GATEWAY,
        customer=user
    )

    telemetry1 = TelemetryData.objects.create(device=device, metric_name="temperature", metric_value=22.3)
    telemetry2 = TelemetryData.objects.create(device=device, metric_name="humidity", metric_value=55.1)

    # Check reverse relation
    telemetry_list = device.telemetry.all()
    assert telemetry1 in telemetry_list
    assert telemetry2 in telemetry_list
    assert telemetry_list.count() == 2
