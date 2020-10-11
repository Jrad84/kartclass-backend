from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
# from kc.api.v1.serializers.tag import TagSerializer
from kc.core.models import Video, Category
from django.contrib.postgres.fields import ArrayField
from drf_writable_nested.serializers import WritableNestedModelSerializer, NestedCreateMixin

class VideoSerializer(WritableNestedModelSerializer, NestedCreateMixin):
    category = CategorySerializer(many=True)
    # tag = TagSerializer()
    
    class Meta:
        model = Video
       
        fields = '__all__'
            
       

    # def create(self, validated_data):
    #     # print(validated_data)
    #     # category_data = validated_data.pop('category')
    #     # # print(category_data) 
    #     return Video.objects.create(**validated_data)
    #     # Video.objects.create(**category_data)
    #     # return video
        
       
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.email)
        instance.longdescription = validated_data.get('longdescription', instance.longdescription)
        instance.category = validated_data.get('category', instance.category)
        # instance.tag = validated_data.get('tag', instance.tag)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.video_file = validated_data.get('video_file', instance.video_file)
        instance.image_file = validated_data.get('image_file', instance.image_file)
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

# class VideoUploadSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=100)
#     longdescription = serializers.TextField(max_length=1000, null=True)    
#     description = serializers.CharField(max_length=150, null=True)
#     category = serializers.ManyToManyField(Category, related_name='category')
#     tag = serializers.ManyToManyField(Tag, related_name='tag')
#     duration = serializers.DecimalField(decimal_places=2, max_digits=9, null=True)
#     video_file = serializers.FileField(null=True)
#     image_file = serializers.FileField(null=True)
    

#     class Meta:
#         model = Video
#         fields = '__all__'

#     def create(self, validated_data):
#         return Video.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.email)
#         instance.longdescription = validated_data.get('longdescription', instance.longdescription)
#         instance.category = validated_data.get('category', instance.category)
#         instance.tag = validated_data.get('tag', instance.tag)
#         instance.duration = validated_data.get('duration', instance.duration)
#         instance.video_file = validated_data.get('video_file', instance.video_file)
#         instance.image_file = validated_data.get('image_file', instance.image_file)
#         instance.save()
#         return instance


   