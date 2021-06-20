from rest_framework import serializers
from kc.core.models import Category, ShopifyCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ShopifyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopifyCategory
        fields = '__all__'