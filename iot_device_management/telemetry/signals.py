from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.cache import cache

from .models import TelemetryData


@receiver(post_save, sender=TelemetryData)
def update_device_last_seen(sender, instance, created, **kwargs):
    if not created:
        return

    device = instance.device
    timestamp = now()

    cache_key = f"device:last_seen:{device.id}"
    cache.set(cache_key, timestamp, timeout=60 * 60)

    device.last_seen = timestamp
    device.save(update_fields=["last_seen"])
