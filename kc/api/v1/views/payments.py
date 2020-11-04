from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
# from django.conf import settings
import os
from django.utils.encoding import smart_str
from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import datetime
from kc.settings.base import STRIPE_SECRET_KEY
from kc.core.models import Category
from kc.users.models import CustomUser

from kc.api.v1.serializers.payments import (

    ChargeSerializer,

)


# from kc.core.models import (
#     Customer,
#     Subscription,
#     Plan,
#     Card
# )

import stripe
import decimal


stripe.api_key = STRIPE_SECRET_KEY

# dictionary of prices : Stripe price ids
prices = {100 : 'price_1HXiJ6D9jmvAZt96ZnsmtMNl', 120 : 'price_1HXiJwD9jmvAZt96902N9Vca',
        140: 'price_1HXiKfD9jmvAZt96sQil7iYy', 160 : 'price_1HXiLKD9jmvAZt96fEOgWA6B', 250 : 'price_1HXiM0D9jmvAZt96Xt09e45V'}

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
      


class ChargeListView(StripeView, generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    queryset = ''
    
        
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)
        amount = request.data.get('price')
        if amount > 0:
            price = prices[amount / 100]
        category = request.data.get('category')
       
        # success = 'http://127.0.0.1:3000/payment-success'
        # cancel = 'http://127.0.0.1:3000/cancelled/'
        user.is_member = True
        success = 'https://kartclass-nuxt.herokuapp.com/payment-success'
        cancel = 'https://kartclass-nuxt.herokuapp.com/cancelled/'
        
        
        if amount > 0:
            checkout_session = stripe.checkout.Session.create(
                            payment_method_types = ['card'],
                            mode='payment',
                            line_items = [{
                                'price': price,
                                'quantity': 1
                            }],
                            success_url = success,
                            cancel_url = cancel
                            
                )

            if (checkout_session):
                user.category.append(category)
            
                user.save(update_fields=["category", "is_member"])
            return Response({'sessionId': checkout_session['id']},status=status.HTTP_202_ACCEPTED)
        
        # user.category.append(category)
        user.save(update_fields=[ "is_member"])
        return Response(status=status.HTTP_202_ACCEPTED)


