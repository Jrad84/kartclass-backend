from django.contrib.auth import get_user_model, hashers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from kc.users.models import CustomUser


class UserRetrieveSerializer(serializers.ModelSerializer):
    """Retrieve serializer for `Users`.
    Contains fields:
    - `uuid`
    - `name`
    """

    class Meta:
        model = get_user_model()
        # category = CategorySerializer()
        fields = (
           "__all__"
           
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
            "fname",
            "lname",
            "email",
            "password",
            "mail_list",
           
        )


    def create(self, validated_data):
       
       
        validated_data['password'] = hashers.make_password(validated_data.get('password'))
        return super(UserCreateSerializer, self).create(validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
   
    password = serializers.CharField(
        write_only=True,
        
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    token = serializers.CharField(
        min_length=1, write_only=True)
  
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "token",
            "checkout"
        )
    
    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(id=self.request.user)
            
            password = attrs.get('password')
            # token = attrs.get('token')
            user = get_user_model()
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed('Authentication failed', 401)
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.content)
        instance.save()
        return instance


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    
    class Meta:
        fields = ['email', 'password']

    def validate(self, attrs):
        # try:
        email = attrs.get('email')
        password = attrs.get('password')
        user = CustomUser.objects.get(email=email)
            
        user.set_password(password)
        user.save()

        # return (user)
        # except Exception as e:
        #     raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email', 'redirect_url']


from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')