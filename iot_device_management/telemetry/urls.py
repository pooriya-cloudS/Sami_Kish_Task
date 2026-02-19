from django.urls import path
from .views import (
    DeviceTelemetryListAPIView,
    TelemetryStatsAPIView,
    TelemetryListAPIView,
)

urlpatterns = [
    path("telemetry/", DeviceTelemetryListAPIView.as_view()),
    path(
        "devices/<int:id>/telemetry/", TelemetryListAPIView.as_view(), name="telemetry"
    ),
    path(
        "devices/<int:id>/telemetry/stats/",
        TelemetryStatsAPIView.as_view(),
        name="telemetry-stats",
    ),
]
