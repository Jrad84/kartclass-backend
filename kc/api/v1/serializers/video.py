from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Video, Category
from django.contrib.postgres.fields import ArrayField
from drf_writable_nested.serializers import WritableNestedModelSerializer, NestedCreateMixin

class VideoSerializer(WritableNestedModelSerializer, NestedCreateMixin):
   
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())
    
    class Meta:
        model = Video   
        fields = '__all__'

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.longdescription = validated_data.get('longdescription', instance.longdescription)
        instance.categories = validated_data.get('category', instance.category)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.video_high_url = validated_data.get('video_high_url', instance.video_high_url)
        instance.video_low_url = validated_data.get('video_low_url', instance.video_low_url)
        instance.image1_url = validated_data.get('image1_url', instance.image1_url)
        instance.image2_url = validated_data.get('image2_url', instance.image2_url)
        instance.document = validated_data.get('document', instance.document)
        instance.release_order = validated_data.get('release_order', instance.release_order)
        
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

class VideoViewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Video
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.views += 1
       
        instance.save()
        return instance
