from django.db import models
from devices.models import Device


class TelemetryData(models.Model):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="telemetry"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    metric_name = models.CharField(max_length=50)
    metric_value = models.FloatField()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.device.name} - {self.created_at}"
