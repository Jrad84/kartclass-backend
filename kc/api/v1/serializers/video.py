from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Video, Category

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Video
        fields = ('id', 'title', 'longdescription', 'description',
                  'category', 'video_file', 'image_file')