from django.contrib.auth import get_user_model, hashers
from rest_framework import serializers
from core.models import Category
from api.v1.serializers.category import CategorySerializer
from pinax.stripe.models import Customer
import stripe


class UserRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve serializer for `Users`.
    Contains fields:
    - `uuid`
    - `name`
    """

    class Meta:
        model = get_user_model()
        category = CategorySerializer()
        fields = (
            "id",
            "name",
            "category"
            "is_member",
            "category",
            "stripe_id"
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """Create serializer for `Users`.
    Contains fields:
    - `uuid`
    - `name`
    - `email`
    - `password`
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "name",
            "email",
            "password",
            "is_member",
            "category",
            "stripe_id"
        )


    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data.get('password'))
        return super(UserCreateSerializer, self).create(validated_data)