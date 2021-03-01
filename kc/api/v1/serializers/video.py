from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
# from kc.api.v1.serializers.tag import TagSerializer
from kc.core.models import Video, Category
from django.contrib.postgres.fields import ArrayField
from drf_writable_nested.serializers import WritableNestedModelSerializer, NestedCreateMixin

class VideoSerializer(WritableNestedModelSerializer, NestedCreateMixin):
    # category = CategorySerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())
    
    class Meta:
        model = Video   
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.longdescription = validated_data.get('longdescription', instance.longdescription)
        instance.categories = validated_data.get('category', instance.category)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.video_url = validated_data.get('video_url', instance.video_url)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.document = validated_data.get('document', instance.document)
        
        instance.save()
        return instance

class VideoLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes += 1
       
        instance.save()
        return instance


class VideoUnLikeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Video
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes -= 1
       
        instance.save()
        return instance
