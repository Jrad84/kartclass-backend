from rest_framework import viewsets, generics, mixins, status
from kc.api.v1.serializers.worksheet import WorksheetSerializer
from rest_framework import permissions
from rest_framework.response import Response
from kc.core.models import Worksheet

class WorksheetView(viewsets.ModelViewSet):
    serializer_class = WorksheetSerializer
    queryset = Worksheet.objects.all()
    permission_classes = [permissions.AllowAny]


class WorksheetUploadView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        return Worksheet.objects.get(pk=uid)

    def post(self, request):
        data=request.data
        serializer = WorksheetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
        worksheet = self.get_object(pk=data['id'])
        serializer = WorksheetSerializer(worksheet, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data=request.data
        worksheet = self.get_object(pk=data['id'])
        worksheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)