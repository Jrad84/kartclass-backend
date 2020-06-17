from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from api.v1.permissions.user import UserPermission
from api.v1.serializers.user import UserCreateSerializer, UserRetrieveSerializer


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet,):

    """`User` view set."""

    """
    
    Notes:
    - Only makes use of active user accounts.
    
    """

    queryset = get_user_model().objects.filter(is_active=True).all()
    permission_classes = (UserPermission,)

    # Change lookup field from `pk` to `uuid`.
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        return UserRetrieveSerializer