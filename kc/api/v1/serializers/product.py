from rest_framework import serializers
from kc.core.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity += validated_data.get('quantity', instance.quantity)
        instance.image = validated_data.get('image', instance.image)
       
        instance.save()
        return instance