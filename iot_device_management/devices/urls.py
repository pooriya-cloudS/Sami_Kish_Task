from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import DeviceViewSet, TelemetryStatsAPIView

router = DefaultRouter()
router.register(r"devices", DeviceViewSet)

urlpatterns = router.urls
