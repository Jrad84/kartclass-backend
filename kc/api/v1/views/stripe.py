from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.encoding import smart_str
from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from pinax.stripe.actions import customers
# from rest_framework.permissions import IsAuthenticated, AllowAny
import datetime
import kc.settings as app_settings
from accounts.models import CustomUser
from api.v1.serializers.stripe import (
    SubscriptionSerializer,
    CurrentCustomerSerializer,
    CustomerSerializer,
    SubscriptionSerializer,
    CardSerializer,
    CancelSerializer,
    ChargeSerializer,
    InvoiceSerializer,
    EventSerializer,
    WebhookSerializer,
    EventProcessingExceptionSerializer,
    PlanSerializer
)

from pinax.stripe.models import (
    Event,
    Customer,
    Subscription,
    EventProcessingException,
    Plan,
    Card
)
import json
from json import JSONEncoder

import stripe


stripe.api_key = settings.PINAX_STRIPE_SECRET_KEY

class StripeView(APIView):
    """ Generic API StripeView """
    permission_classes = (permissions.IsAuthenticated, )

    def get_current_subscription(self):
        try:
            return self.request.user.customer.subscription
        except Subscription.DoesNotExist:
            return None

    def get_customer(self):
        try:
            return self.request.user.customer
        except ObjectDoesNotExist:
            print('Customer does not exist')
        #     customer = customers.create(user = self.request.user)
        #     # print(customer.stripe_id)
        #     # self.request.user.stripe_id = customer.stripe_id
        #     return customer




class CurrentCustomerDetailView(StripeView, generics.RetrieveAPIView):
    """ See the current customer/user payment details """
    
    serializer_class = CurrentCustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get_object(self):
        return self.get_customer()

    def post(self, request, *args, **kwargs):
        
        user = CustomUser.objects.get(email=request.user)
        # user1 = CustomUser.objects.get(email='user')
        print(user)
        plan = request.data['stripe_id']
        # stripe_id = plan.get('stripe_id')
        source = request.data['source']
        source_id = source.get('source').get('id')
       
        result = customers.create(user=user, card=source_id, plan=plan, quantity=1)
        print(result)
        customer = result.stripe_id
        print(customer)
        user.stripe_id = customer
        user.is_member = True
        user.save(update_fields=["stripe_id", "is_member"])
        
        serializer = CurrentCustomerSerializer(data=request.data)
        
        if serializer.is_valid():
            print('Nice, Serializer is VALID !!!!')
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            # print(serializer)
            print("Serializer NOT VALID - FAIL!!!")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionView(StripeView):
    """ See, change/set the current customer/user subscription plan """
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **kwargs):
        current_subscription = self.get_current_subscription()
        serializer = SubscriptionSerializer(current_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            stripe_plan = validated_data.get('stripe_plan', None)
            customer = self.get_customer()
            subscription = customer.subscribe(stripe_plan)
            return Response(subscription, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
# class SubscriptionView(StripeView):
#     """ See, change/set the current customer/user subscription plan """
#     serializer_class = SubscriptionSerializer
#     permission_classes = (permissions.AllowAny,)
#     def get(self, request, *args, **kwargs):
#         current_subscription = self.get_current_subscription()
#         serializer = SubscriptionSerializer(current_subscription)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.serializer_class(data=request.data)

#             if serializer.is_valid():
#                 validated_data = serializer.validated_data
#                 # stripe_plan = validated_data.get('stripe_plan', None)
#                 # print(stripe_plan)
#                 # customer = self.get_customer()
#                 # stripe_id = customer.stripe_id
                
#                 start_time = datetime.datetime.now()
#                 subscription = stripe.Subscription.create(validated_data, start_time, quantity=1,  status="active")
#                 #subscription = customer.subscribe(stripe_plan)

#                 return Response(subscription, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except stripe.StripeError as e:
#             from django.utils.encoding import smart_str

#             error_data = {u'error': smart_str(e) or u'Unknown error'}
#             return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


class ChangeCardView(StripeView):
    """ Add or update customer card details """
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                customer = self.get_customer()
                card_token_response = customer.create_card_token(validated_data)
                token = card_token_response[0].get('id', None)
                customer.update_card(token)
                send_invoice = customer.card_fingerprint == ""

                if send_invoice:
                    customer.send_invoice()
                    customer.retry_unpaid_invoices()

                return Response(validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except stripe.CardError as e:
            error_data = {u'error': smart_str(e) or u'Unknown error'}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


class CancelView(StripeView):
    """ Cancel customer subscription """
    serializer_class = CancelSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                customer = self.get_customer()
                customer.cancel()
                return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except stripe.StripeError as e:
            error_data = {u'error': smart_str(e) or u'Unknown error'}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


class PlanListView(StripeView, generics.ListAPIView):
    """ List all current plans """
    permission_classes = (permissions.AllowAny,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    


class ChargeListView(StripeView, generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer

    def get_queryset(self):
        customer = self.get_customer()
        charges = customer.charges.all()
        return charges


class InvoiceListView(StripeView, generics.ListAPIView):
    """ List customer invoices """
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        customer = self.get_customer()
        invoices = customer.invoices.all()
        return invoices


class EventListView(StripeView, generics.ListAPIView):
    """ List customer events """
    serializer_class = EventSerializer

    def get_queryset(self):
        customer = self.get_customer()
        events = customer.event_set.all()
        return events


class WebhookView(StripeView):
    serializer_class = WebhookSerializer

    def validate_webhook(self, webhook_data):
        webhook_id = webhook_data.get('id', None)
        webhook_type = webhook_data.get('type', None)
        webhook_livemode = webhook_data.get('livemode', None)
        is_valid = False

        if webhook_id and webhook_type and webhook_livemode:
            is_valid = True
        return is_valid, webhook_id, webhook_type, webhook_livemode

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                webhook_data = validated_data.get('data', None)

                is_webhook_valid, webhook_id, webhook_type, webhook_livemode = self.validate_webhook(webhook_data)

                if is_webhook_valid:
                    if Event.objects.filter(stripe_id=webhook_id).exists():
                        obj = EventProcessingException.objects.create(
                            data=validated_data,
                            message="Duplicate event record",
                            traceback=""
                        )

                        event_processing_exception_serializer = EventProcessingExceptionSerializer(obj)
                        return Response(event_processing_exception_serializer.data, status=status.HTTP_200_OK)
                    else:
                        event = Event.objects.create(
                            stripe_id=webhook_id,
                            kind=webhook_type,
                            livemode=webhook_livemode,
                            webhook_message=validated_data
                        )
                        event.validate()
                        event.process()
                        event_serializer = EventSerializer(event)
                        return Response(event_serializer.data, status=status.HTTP_200_OK)
                else:
                    error_data = {u'error': u'Webhook must contain id, type and livemode.'}
                    return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except stripe.StripeError as e:
            error_data = {u'error': smart_str(e) or u'Unknown error'}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)