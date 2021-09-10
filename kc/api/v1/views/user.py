from django.contrib.auth import get_user_model
from rest_framework import views, mixins, viewsets, generics, status, permissions
from kc.api.v1.permissions.user import UserPermission
from django.http import JsonResponse
from django.urls import reverse
from kc.api.v1.serializers.user import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from django.http import HttpResponsePermanentRedirect
from braces.views import CsrfExemptMixin
from django.views.decorators.csrf import csrf_exempt
from kc.utils import send_email
import logging

logger = logging.getLogger(__name__)




class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = ['local', 'http', 'https', '127.0.0.1']

class UserViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin, generics.GenericAPIView):

    """`User` view set."""

    """
    
    Notes:
    - Only makes use of active user accounts.
    
    """

    queryset = get_user_model().objects.filter(is_active=True).all()
   
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserRetrieveSerializer

    def get(self, request):
        permission_classes = (permissions.IsAdminUser, )
        users = get_user_model().objects.filter(is_active=True).all().values()
        return JsonResponse({"users": list(users)})

  
class UpdateUserView(mixins.RetrieveModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin, generics.GenericAPIView, CsrfExemptMixin):

    serializer = UserUpdateSerializer
    # authentication_classes = []
    permission_classes = (permissions.IsAuthenticated,)

    @csrf_exempt
    def patch(self, request):
       
        user = CustomUser.objects.get(email=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
       
        serializer = self.serializer_class(data=request.data)
       
        email = request.data.get('email', '')
        if serializer.is_valid():
            
            if CustomUser.objects.filter(email=email).exists():
               
                user = CustomUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = 'https://kartclass-engine.xyz'
                relativeLink = reverse(
                    'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

                redirect_url = request.data.get('redirect_url', '')
                
                # CHANGE HERE FOR DEV / PROD
                absurl = current_site + relativeLink 
               
                email_body = 'Hey ' + user.fname +', \n Use the link below to reset your password  \n' + \
                    absurl+"?redirect_url="+redirect_url
                data = {'email_body': email_body, 'to_email': (user.email, ''),
                        'email_subject': 'Reset your KartClass password'}
                send_email(data)
               
               
                return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            error = "No user found with that email address"
                
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')
        
        #url = 'http://127.0.0.1:3000/reset-password'
        url = 'https://www.kartclass.com/reset-password'

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(url +'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(url +'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (permissions.AllowAny,)

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    @csrf_exempt
    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        print(sz)
        
        sz.is_valid(raise_exception=True)
        refresh = sz['refresh']['0']
        sz.refresh = str(refresh)
        sz.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

 

class PopupView(generics.ListAPIView):

    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        user = CustomUser.objects.get(email=request.user)
        try:
            user.popup = request.data['popup']
            user.save()

            return Response(status=status.HTTP_200_OK)
        
        except:

            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
       