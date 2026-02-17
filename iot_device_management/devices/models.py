from django.db import models
from users.models import User


class Device(models.Model):
    SENSOR = "sensor"
    GATEWAY = "gateway"
    ACTUATOR = "actuator"

    DEVICE_TYPE_CHOICES = [
        (SENSOR, "Sensor"),
        (GATEWAY, "Gateway"),
        (ACTUATOR, "Actuator"),
    ]

    serial_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE_CHOICES)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
