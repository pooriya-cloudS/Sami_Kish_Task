from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserSerializer
from iot_device_management.paginations import StandardPagePagination


@extend_schema(tags=["Users"])
class UserListCreateView(APIView):
    pagination_class = StandardPagePagination
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = self.serializer_class(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
