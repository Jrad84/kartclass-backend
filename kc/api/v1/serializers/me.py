from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from kc.users.models import CustomUser

class MeRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve serializer for authenticated user (`Me`).
    Contains fields:
    - `uuid`
    - `email`
    - `name`
    - `is_staff`
    - `date_created`
    """

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "name",
            "is_staff",
            "date_created",
            "category"
        )

class MeUpdateSerializer(serializers.ModelSerializer):
    """Update serializer for authenticated user (`Me`).
    Contains fields:
    - `uuid`
    - `email`
    - `name`
    """

    class Meta:
        model = get_user_model()
        fields = (
            "pk",
            "email",
            "password"
           
        )

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    oldPassword = serializers.CharField(required=True)
        
    newPassword = serializers.CharField(required=True )