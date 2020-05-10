from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers.user import (UserDetailSerializer,
                                           UserUpdateSerializer)


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Endpoint for getting the authenticated user. """

        user = request.user
        serializer = UserDetailSerializer(user)

        return Response(serializer.data)

    def patch(self, request):
        """ Endpoint for updating the authenticated user. """

        user = request.user
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
