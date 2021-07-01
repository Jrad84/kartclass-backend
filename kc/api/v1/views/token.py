from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['fname'] = user.fname
        token['lname'] = user.lname
        token['email'] = user.email
        token['category'] = user.category
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer