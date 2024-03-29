from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from kc.api.v1.serializers.product import ProductSerializer
from kc.core.models import Product

class ProductListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,
                    ):

    serializer_class = ProductSerializer
   
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.all()

class PurchaseProductVieww(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet,
                    ):

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Product.objects.all()

    def get_object(self, pk):
        return Product.objects.get(pk=pk)

    def post(self, pk):
        data = request.data
        
class ProductUploadView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, pk):
        return Product.objects.get(pk=pk)

    def post(self, request):
        data=request.data
        size = str(data.get("size")[0])
        data['size'] = size
        serializer = UpdateProductSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
      
        product = self.get_object(pk=data['id'])
       
        serializer = UpdateProductSerializer(video, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data=request.data
        product = self.get_object(pk=data['id'])
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)