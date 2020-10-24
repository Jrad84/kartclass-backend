from rest_framework import serializers
from kc.core.models import Article

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'image', 'document', 'likes')

class ArticleLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes += 1
       
        instance.save()
        return instance


class ArticleUnLikeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Article
        fields = '__all__'

    def update(self, instance, validated_data):
        
        instance.likes -= 1
       
        instance.save()
        return instance

