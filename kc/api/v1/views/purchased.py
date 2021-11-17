from rest_framework import viewsets, generics, mixins, status
from kc.api.v1.serializers.purchased import PurchasedDateSerializer
from rest_framework import permissions
from rest_framework.response import Response
from kc.core.models import PurchasedDate

class PurchasedDateView(viewsets.ModelViewSet):
    serializer_class = PurchasedDateSerializer
    queryset = PurchasedDate.objects.all()
    permission_classes = [permissions.AllowAny]


class PurchasedDatePostView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, pk):
        return PurchasedDate.objects.get(pk=uid)

    def post(self, request):
        data=request.data
        serializer = PurchasedDateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)