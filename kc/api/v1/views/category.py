from rest_framework import viewsets, generics, mixins
from kc.api.v1.serializers.category import CategorySerializer, ShopifyCategorySerializer
from rest_framework import permissions
from kc.core.models import Category, ShopifyCategory

class CategoryView(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny,]
    authentication_classes = []

class ShopifyCategoryView(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = ShopifyCategorySerializer
    queryset = ShopifyCategory.objects.all()
    permission_classes = [permissions.AllowAny,]
    authentication_classes = []