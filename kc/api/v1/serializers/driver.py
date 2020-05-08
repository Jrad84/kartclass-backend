from rest_framework import serializers
from core.models import Driver

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'first_name', 'last_name')