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
            "id",
            "email",
            "password"
           
        )
    
    # def validate(self, attrs):
    #     try:
    #         print(attrs)
    #         password = attrs.get('password')
    #         email = attrs.get('email')
    #         uid = attrs.get('id')
    #         # print(uid)
    #         user = CustomUser.objects.get(id=uid)
    #         # print(user)
    #         user.set_password(password)
    #         user.save()

    #         return user
    #     except Exception as e:
    #         raise AuthenticationFailed('There was a problem', 401)
    #     return super().validate(attrs)