from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters, generics, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from kc.api.v1.permissions.user import UserPermission
from django.http import JsonResponse
from kc.api.v1.serializers.user import (
    UserCreateSerializer, 
    UserRetrieveSerializer, 
    UserUpdateSerializer, 
    RefreshTokenSerializer
)
from kc.api.v1.serializers.category import CategorySerializer
from rest_framework.response import Response
from braces.views import CsrfExemptMixin
from django.views.decorators.csrf import csrf_exempt

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
    # category = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'category__id')


    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserRetrieveSerializer

    def get(self, request):
        
        users = get_user_model().objects.filter(is_active=True).all().values()

        return JsonResponse({"users": list(users)})
      
class UpdateUserView(mixins.RetrieveModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin, generics.GenericAPIView, CsrfExemptMixin):

    serializer = UserUpdateSerializer
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticated,)

    @csrf_exempt
    def patch(self, request):
       
        user = CustomUser.objects.get(email=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    @csrf_exempt
    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

 

        