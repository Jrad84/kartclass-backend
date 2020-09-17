from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.serializers.me import MeRetrieveSerializer, MeUpdateSerializer
from kc.users.models import CustomUser
from rest_framework.response import Response

class MeView(generics.RetrieveUpdateAPIView):
    """Authenticated user view."""

    """
    TODO: Add delete.
    """

    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH",):
            return MeUpdateSerializer

        return MeRetrieveSerializer

    def get_object(self):
        return self.request.user

    @csrf_exempt
    def patch(self, request):
        
        user = self.request.user
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)