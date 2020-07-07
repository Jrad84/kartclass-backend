from rest_framework import viewsets
from api.v1.serializers.driver import DriverSerializer
from rest_framework import permissions
from core.models import Driver

class DriverView(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]