from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import exceptions, filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from api.v1.serializers.user import UserSerializer, UserListSerializer, UserDetailSerializer



class UserViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet,):

    queryset = get_user_model().objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ('username',)
    ordering = ('-id',)
    ordering_fields = (
        'id',
        'username',
        'date_joined',
        'last_login',
    )
    filterset_fields = (
        'is_active',
        'is_staff',
        'is_superuser',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer

        return UserSerializer

    # @action(detail=True, methods=['GET'], name='Salesperson invoices')
    # def invoices(self, request, pk=None):
    #     """Get invoices made by a salesperson."""

    #     user = get_object_or_404(self.queryset, pk=pk)

    #     invoices = Invoice.objects.filter(
    #         salesperson=user).order_by('-datetime_created')
    #     serializer = InvoiceListSerializer(invoices, many=True)

    #     return Response(serializer.data)
