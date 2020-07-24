from rest_framework import viewsets, generics, mixins
from api.v1.serializers.product import ProductSerializer
from rest_framework import permissions
from core.models import Product

class ProductView(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny,]