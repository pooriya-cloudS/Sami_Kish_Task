from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    header_name = "X-API-KEY"

    def authenticate(self, request):
        api_key = request.headers.get(self.header_name)

        if not api_key:
            return None

        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive API key")

        key_obj.last_used_at = timezone.now()
        key_obj.save(update_fields=["last_used_at"])

        return (None, key_obj)
