from rest_framework import serializers
from core.models import Article
from api.v1.serializers.category import CategorySerializer
from api.v1.serializers.driver import DriverSerializer

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    driver = DriverSerializer

    class Meta:
        model = Article
        fields = ('id', 'driver', 'description', 'category',
                  'picture')
