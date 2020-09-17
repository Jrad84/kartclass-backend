from rest_framework import serializers
from kc.core.models import Tag

class TagSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Tag
        fields = '__all__'