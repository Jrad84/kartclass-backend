from rest_framework import serializers
from kc.utils import register_social_user
import kc.fb as fb

class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    code = serializers.CharField()

    def validate_auth_token(self, code):
        user_data = fb.Facebook.validate(code)
        print('serializer class: ', user_data)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )