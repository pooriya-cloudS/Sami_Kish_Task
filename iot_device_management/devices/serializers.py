from rest_framework import serializers
from django.core.cache import cache

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    last_seen = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = "__all__"

    def get_last_seen(self, obj):
        cache_key = f"device:last_seen:{obj.id}"
        return cache.get(cache_key) or obj.last_seen
