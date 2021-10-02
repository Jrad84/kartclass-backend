from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Podcast, Category
from django.contrib.postgres.fields import ArrayField
from drf_writable_nested.serializers import WritableNestedModelSerializer, NestedCreateMixin

class PodcastSerializer(WritableNestedModelSerializer, NestedCreateMixin):
   
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())
    
    class Meta:
        model = Podcast   
        fields = '__all__'

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.category = validated_data.get('category', instance.category)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.image1_url = validated_data.get('image1_url', instance.image1_url)
        instance.podcast_link = validated_data.get('podcast_link', instance.podcast_link)
        
        instance.save()
        return instance

class PodcastLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Podcast
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes += 1
       
        instance.save()
        return instance


class PodcastUnLikeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Podcast
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes -= 1
       
        instance.save()
        return instance
