from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import FilterSet, filters
from telemetry.models import TelemetryData
from .models import Device
from .serializers import DeviceSerializer
from iot_device_management.paginations import StandardPagePagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Min, Max, Avg
from drf_spectacular.utils import extend_schema


class DeviceFilter(FilterSet):
    customer_id = filters.NumberFilter(field_name="customer_id")
    device_type = filters.CharFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = Device
        fields = ["customer_id", "device_type", "is_active"]


@extend_schema(tags=["Devices"])
class DeviceViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = StandardPagePagination
    filterset_class = DeviceFilter


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
