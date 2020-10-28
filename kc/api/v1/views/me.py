from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.serializers.me import *
from kc.users.models import CustomUser
from rest_framework.response import Response

class MeView(generics.RetrieveUpdateAPIView, generics.GenericAPIView):
    """Authenticated user view."""

    """
    TODO: Add delete.
    """

    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH",):
            return MeUpdateSerializer
        print(self.request.data)
        return MeRetrieveSerializer

    def get_object(self):
        return self.request.user

    @csrf_exempt
    def patch(self, request):
       
        user = self.get_object()
        serializer = MeUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)

class ChangeEmailView(generics.UpdateAPIView):

    serializer_class = ChangeEmailSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
            obj = self.request.user
            return obj

    def patch(self, request, *args, **kwargs):
            user = self.get_object()
          
            serializer = self.get_serializer(data=request.data, partial=True)
           
            if serializer.is_valid():
                # Check old email
               
                if serializer.data.get("oldEmail") != user.email:
                    return Response({"old_email": ["Wrong email."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                user.email = serializer.data.get("newEmail")
                user.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Email updated successfully',
                    'data': [],
                    'user': user
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = CustomUser
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def patch(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data, partial=True)
            print(serializer)
            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("oldPassword")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("newPassword"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': [],
                    'user': user
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)