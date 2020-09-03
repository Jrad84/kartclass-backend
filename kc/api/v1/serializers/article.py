from rest_framework import serializers
from kc.core.models import Article

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'image', 'document')
