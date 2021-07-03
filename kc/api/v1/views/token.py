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

        # Add custom claims
        # token['fname'] = user.fname
        # token['lname'] = user.lname
        # token['email'] = user.email
        # token['category'] = user.category
        # ...

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        user = CustomUser.objects.get(email=self.user.email)
        print(user)
        user.token = str(refresh.access_token)
        user.save()
        # self.user.token = data['access']
        # Add extra responses here
        # data['email'] = self.user.email
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    print('token view here')
    serializer_class = MyTokenObtainPairSerializer
    print(serializer_class)

    # def post(self, request):
    #     print(request.data)
    #     user = CustomUser.objects.get(email=request.data['email'])
    #     print(user.token)
        
    #     return Response({'token': user.token}, status=status.HTTP_200_OK )

        # add token to user model and return token in response so it can be added in request header to /me

       
        # print(serializer)
       
        # if serializer.is_valid():
        #     # user = CustomUser.objects.get(email=request.data['email'])
        #     # print(user)
        #     # user.token = request.data['email']
        #     # user.save(update_fields="token")
        #     return Response({'success': True, 'message': 'ok'}, status=status.HTTP_200_OK)
        # # serializer = self.serializer_class(data=request.data)
        # # print(serializer)

        # if serializer.is_valid():
        #     return Response({'success': True, 'message': 'ok'}, status=status.HTTP_200_OK)
        # return Response({'success': False, 'message': 'fuck no'}, status=status.HTTP_400_BAD_REQUEST)
    