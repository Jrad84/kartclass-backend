from rest_framework import serializers
from kc.core.models import Worksheet, Category

class WorksheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worksheet
        category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.document = validated_data.get('document', instance.document)
        instance.order_id = validated_data.get('order_id', instance.order_id)

        instance.save()
        return instance

class WorksheetLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worksheet
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes += 1
       
        instance.save()
        return instance


class WorksheetUnLikeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Worksheet
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes -= 1
       
        instance.save()
        return instance

