from rest_framework import viewsets, generics, mixins
from api.v1.serializers.registration import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from core.models import Registration
import datetime

class RegistrationView(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = RegistrationSerializer
    queryset = Registration.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user.is_staff:
            return Response(status=status.HTTP_400_BAD_REQUEST)
