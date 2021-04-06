from rest_framework import serializers
from kc.core.models import Blog

class BlogSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Blog   
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.body = validated_data.get('body', instance.body)
        instance.author = validated_data.get('author', instance.author)
        instance.seo_tags = validated_data.get('seo_tags', instance.seo_tags)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        
        instance.save()
        return instance