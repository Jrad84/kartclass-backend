from rest_framework import serializers
from kc.core.models import MailList

class MailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailList
        fields = '__all__'