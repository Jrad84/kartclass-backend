from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from rest_framework.response import Response

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   
    authentication_classes = []
   
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
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # print(data)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['email'] = self.user.email
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
   
    serializer_class = MyTokenObtainPairSerializer
    

    def post(self, request):
        permission_classes = (permissions.AllowAny,)
        serializer_class = MyTokenObtainPairSerializer
        # serializer = self.serializer_class(data=request.data)
        # print(serializer)

        # if serializer.is_valid():
        #     return Response({'success': True, 'message': 'ok'}, status=status.HTTP_200_OK)
        # return Response({'success': False, 'message': 'fuck no'}, status=status.HTTP_400_BAD_REQUEST)
    