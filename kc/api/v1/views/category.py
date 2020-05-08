from rest_framework import viewsets
from api.v1.serializers.category import CategorySerializer
from core.models import Category

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()