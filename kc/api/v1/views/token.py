from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, status
from rest_framework.response import Response
from kc.users.models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
       
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        user = CustomUser.objects.get(email=self.user.email)
       
        user.token = str(refresh.access_token)
        user.save()
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
   
    serializer_class = MyTokenObtainPairSerializer
   