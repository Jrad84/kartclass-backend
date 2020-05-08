from rest_framework import serializers
from api.v1.serializers.category import CategorySerializer
from api.v1.serializers.driver import DriverSerializer
from core.models import Video

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    driver = DriverSerializer

    class Meta:
        model = Video
        fields = ('id', 'title', 'driver', 'description',
                  'category', 'video_file', 'image_file')