from rest_framework import viewsets, generics, mixins
from api.v1.serializers.category import CategorySerializer
from rest_framework import permissions
from core.models import Category

class CategoryView(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]