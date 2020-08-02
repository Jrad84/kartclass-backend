from rest_framework import viewsets
from kc.api.v1.serializers.driver import DriverSerializer
from rest_framework import permissions
from kc.core.models import Driver

class DriverView(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]