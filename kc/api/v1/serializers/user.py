from django.contrib.auth import get_user_model, hashers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from kc.core.models import Category
from kc.api.v1.serializers.category import CategorySerializer

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

class ResetPasswordSerializer(serializers.Serializer):
    serializer = UserRetrieveSerializer()
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            user = get_user_model()
            user = user.objects.get(attrs.user) 
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Something is wrong', 401)
            
            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('Authentication failed', 401)
        return super().validate(attrs)