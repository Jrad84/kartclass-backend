from rest_framework import serializers
from kc.core.models import Article

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'image', 'document', 'likes')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.document = validated_data.get('document', instance.document)

        instance.save()
        return instance

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

