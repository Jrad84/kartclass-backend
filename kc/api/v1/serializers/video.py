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
        # instance.shopify_id = validated_data.get.get('shopify_id', instance.shopify_id)
        instance.description = validated_data.get('description', instance.description)
        instance.longdescription = validated_data.get('longdescription', instance.longdescription)
        instance.categories = validated_data.get('category', instance.category)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.video_url = validated_data.get('video_url', instance.video_url)
        instance.image1_url = validated_data.get('image1_url', instance.image1_url)
        instance.image2_url = validated_data.get('image2_url', instance.image2_url)
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
