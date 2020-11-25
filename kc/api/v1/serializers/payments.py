from rest_framework import serializers
from kc.core.models import Charge


ModelSerializer = serializers.ModelSerializer
Serializer = serializers.Serializer


class ChargeSerializer(ModelSerializer):
    class Meta:
        model = Charge
        fields = '__all__'

