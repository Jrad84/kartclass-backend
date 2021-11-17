from rest_framework import serializers
from kc.core.models import PurchasedDate, Category

class PurchasedDateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedDate
        category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.purchased = validated_data.get('purchased', instance.purchased)
        instance.category = validated_data.get('category', instance.category)

        instance.save()
        return instance


class PurchasedDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedDate
        fields = '__all__'

