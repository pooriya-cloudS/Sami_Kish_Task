from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils.dateparse import parse_datetime
from .models import TelemetryData
from .serializers import TelemetrySerializer
from iot_device_management.paginations import StandardPagePagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Min, Max, Avg
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    tags=["Telemetry"],
    parameters=[
        OpenApiParameter("start_date", type=str),
        OpenApiParameter("end_date", type=str),
    ],
)
class DeviceTelemetryListAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TelemetrySerializer

@extend_schema(tags=["Telemetry"])
class TelemetryListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TelemetrySerializer
    pagination_class = StandardPagePagination

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

        if start:
            queryset = queryset.filter(timestamp__gte=start)
        if end:
            queryset = queryset.filter(timestamp__lte=end)

        data = queryset.aggregate(
            min_temp=Min("temperature"),
            max_temp=Max("temperature"),
            avg_temp=Avg("temperature"),
            min_humidity=Min("humidity"),
            max_humidity=Max("humidity"),
            avg_humidity=Avg("humidity"),
        )

        return Response(data)
