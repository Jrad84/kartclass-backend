from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.permissions.user import UserPermission
from api.v1.serializers.user import UserCreateSerializer, UserRetrieveSerializer
from api.v1.serializers.category import CategorySerializer
from rest_framework.response import Response
import stripe


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

   # Change user category. Possibly move to questionairre endpoint
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = UserRetrieveSerializer(data=data)
        if serializer.is_valid:
            category = request.data['category']
            user.category = category
            user.save(update_fields=["category"])
            return Response(user, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        