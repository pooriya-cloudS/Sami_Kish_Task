from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import TelemetryData
from .serializers import TelemetrySerializer
from iot_device_management.paginations import StandardCursorPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Min, Max, Avg
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.core.cache import cache
from authentication.permissions import HasAPIKey

@extend_schema(
    tags=["Telemetry"],
    parameters=[
        OpenApiParameter("start_date", type=str),
        OpenApiParameter("end_date", type=str),
    ],
)
class DeviceTelemetryListAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = TelemetrySerializer


@extend_schema(tags=["Telemetry"])
class TelemetryListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TelemetrySerializer
    pagination_class = StandardCursorPagination

    def get_queryset(self):
        device_id = self.kwargs.get("id")
        queryset = TelemetryData.objects.filter(device_id=device_id)

        start = self.request.query_params.get("start_date")
        end = self.request.query_params.get("end_date")

        if start:
            queryset = queryset.filter(timestamp__gte=start)
        if end:
            queryset = queryset.filter(timestamp__lte=end)

        return queryset


@extend_schema(tags=["Telemetry"])
class TelemetryStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        queryset = TelemetryData.objects.filter(device_id=id)

        start = request.query_params.get("start_date")
        end = request.query_params.get("end_date")

        cache_key = f"telemetry:stats:{id}:{start}:{end}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        if start:
            queryset = queryset.filter(timestamp__gte=start)
        if end:
            queryset = queryset.filter(timestamp__lte=end)

        data = queryset.aggregate(
            min_metric_value=Min("metric_value"),
            max_metric_value=Max("metric_value"),
            avg_metric_value=Avg("metric_value"),
        )

        cache.set(cache_key, data, timeout=60 * 5)

        return Response(data)
