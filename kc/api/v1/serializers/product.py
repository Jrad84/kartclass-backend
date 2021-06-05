from rest_framework import serializers
from kc.core.models import Product

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock_level += validated_data.get('stock_level', instance.stock_level)
        instance.size = validated_data.get('size', instance.size)
        instance.image1 = validated_data.get('image1', instance.image1)
        instance.image2 = validated_data.get('image2', instance.image2)
       
        instance.save()
        return instance

class ProductSerializer(models.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

