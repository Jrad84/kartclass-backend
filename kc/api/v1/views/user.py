from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from kc.api.v1.permissions.user import UserPermission
from kc.api.v1.serializers.user import UserCreateSerializer, UserRetrieveSerializer, ResetPasswordSerializer
from kc.api.v1.serializers.category import CategorySerializer
from rest_framework.response import Response



class UserViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet,
    generics.GenericAPIView):

    """`User` view set."""

    """
    
    Notes:
    - Only makes use of active user accounts.
    
    """

    queryset = get_user_model().objects.filter(is_active=True).all()
    permission_classes = (UserPermission,)
    category = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'category__id')

    # Change lookup field from `pk` to `uuid`.
    # lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        return UserRetrieveSerializer


class PasswordResetView(mixins.UpdateModelMixin, generics.GenericAPIView):
    
    serializer_class = ResetPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

 

        