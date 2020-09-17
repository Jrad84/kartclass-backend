from rest_framework import serializers
from kc.api.v1.serializers.category import CategorySerializer
from kc.api.v1.serializers.tag import TagSerializer
from kc.core.models import Video, Category, Tag

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Video
        fields = ('id', 'title', 'longdescription', 'description',
                  'category', 'tag', 'video_file', 'image_file')