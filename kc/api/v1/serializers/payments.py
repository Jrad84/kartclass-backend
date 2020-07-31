from rest_framework import serializers
import kc.settings.local as app_settings
from django.contrib.auth import get_user_model
from pinax.stripe.actions import customers
from pinax.stripe.models import (
    EventProcessingException,
    Event,
    Transfer,
    TransferChargeFee,
    TransferChargeFee,
    Customer,
    Subscription,
    Invoice,
    InvoiceItem,
    Charge,
    Plan,
    Card
)
import stripe

"""
    Model API Serializers
"""
from rest_framework import serializers

ModelSerializer = serializers.ModelSerializer
Serializer = serializers.Serializer

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value

class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        
class EventProcessingExceptionSerializer(ModelSerializer):
    class Meta:
        model = EventProcessingException
        fields = '__all__'


class EventSerializer(ModelSerializer):
    event_processing_exceptions = EventProcessingExceptionSerializer(source='event_processing_exception_serializer_set', many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


# class SubscriptionSerializer(ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = '__all__'

    # def create(self, validated_data):
    #     stripe.Subscription.create()

class SubscriptionSerializer(Serializer):
    class Meta:
        stripe_plan = serializers.ChoiceField(choices=app_settings.PAYMENT_PLANS, required=True)
        model = Subscription
        fields = '__all__'

class ChargeSerializer(ModelSerializer):
    class Meta:
        model = Charge
        fields = '__all__'


class InvoiceItemSerializer(ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'


class InvoiceSerializer(ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    charges = ChargeSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


class CurrentCustomerSerializer(ModelSerializer):
    has_active_subscription = serializers.ReadOnlyField()
    can_charge = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = '__all__'



class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    # def create(self, validated_data):
    #     user = get_user_model()
    #     source = validated_data['source']
    #     plan = validated_data['plan']
    #     currency = 'aud'
        
        
    #     customers.create(name=validated_data['name'], email=validated_data['email'])
    #     return super(CustomerCreateSerializer, self).create(validated_data)

"""
    Custom API Serializers
"""

class CardSerializer(Serializer):
    number = serializers.IntegerField(help_text=u'The card number, as a string without any separators.', required=True)
    exp_month = serializers.IntegerField(help_text=u"Two digit number representing the card's expiration month.", required=True)
    exp_year = serializers.IntegerField(help_text=u"Two or four digit number representing the card's expiration year.", required=True)
    cvc = serializers.IntegerField(help_text=u'Card security code.', required=True)

    name = serializers.CharField(help_text=u"Cardholder's full name.", required=False, allow_null=True)
    address_line1 = serializers.CharField(required=False, allow_null=True)
    address_line2 = serializers.CharField(required=False, allow_null=True)
    address_city = serializers.CharField(required=False, allow_null=True)
    address_zip = serializers.CharField(required=False, allow_null=True)
    address_state = serializers.CharField(required=False, allow_null=True)
    address_country = serializers.CharField(required=False, allow_null=True)



class CancelSerializer(Serializer):
    confirm = serializers.BooleanField(required=True)

    def validate_confirm(self, value):
        if value is False:
            raise serializers.ValidationError(u"Please confirm to continue.")
        return value


class WebhookSerializer(Serializer):
    data = JSONSerializerField(required=True, allow_null=False)