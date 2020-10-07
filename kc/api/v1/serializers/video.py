from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
from kc.api.v1.serializers.tag import TagSerializer
from kc.core.models import Video, Category, Tag
from django.contrib.postgres.fields import ArrayField

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Video
        fields = '__all__'

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

class VideoUploadSerializer(serializers.ModelSerializer):
    category = ArrayField(serializers.CharField(max_length=50))
    tag = ArrayField(serializers.CharField(max_length=50))
    class Meta:
        model = Video
        fields = '__all__'