# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView


# class FacebookLoginView(SocialLoginView):
#     authentication_classes = []
#     adapter_class = FacebookOAuth2Adapter
#     callback_url = "http://localhost:3000/login"
#     client_class = OAuth2Client
#     print(adapter_class)



# from django.http import JsonResponse
# from rest_framework import generics, permissions, status, views
# from rest_framework.response import Response
# from requests.exceptions import HTTPError
 
# from social_django.utils import load_strategy, load_backend
# from social_core.backends.oauth import BaseOAuth2
# from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
# from kc.api.v1.serializers.social import SocialSerializer
 
# class SocialLoginView(generics.GenericAPIView):
#     """Log in using facebook"""
#     serializer_class = SocialSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         """Authenticate user through the provider and access_token"""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         provider = serializer.data.get('provider', None)
#         strategy = load_strategy(request)
 
#         try:
#             backend = load_backend(strategy=strategy, name=provider,
#             redirect_uri=None)
 
#         except MissingBackend:
#             return Response({'error': 'Please provide a valid provider'},
#             status=status.HTTP_400_BAD_REQUEST)
#         try:
#             if isinstance(backend, BaseOAuth2):
#                 access_token = serializer.data.get('access_token')
#             user = backend.do_auth(access_token)
#         except HTTPError as error:
#             return Response({
#                 "error": {
#                       "access_token": "Invalid token",
#                     "details": str(error)
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except AuthTokenError as error:
#             return Response({
#                 "error": "Invalid credentials",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
 
#         try:
#             authenticated_user = backend.do_auth(access_token, user=user)
        
#         except HTTPError as error:
#             return Response({
#                 "error":"invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         except AuthForbidden as error:
#             return Response({
#                 "error":"invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
 
#         if authenticated_user and authenticated_user.is_active:
#             #generate JWT token
#             login(request, authenticated_user)
#             data={
#                 "token": jwt_encode_handler(
#                     jwt_payload_handler(user)
#                 )}
#             #customize the response to your needs
#             response = {
#                 "email": authenticated_user.email,
#                 "username": authenticated_user.username,
#                 "token": data.get('token')
#             }
#             return Response(status=status.HTTP_200_OK, data=response)