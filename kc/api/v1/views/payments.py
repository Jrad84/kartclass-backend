from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from kc.settings.base import STRIPE_SECRET_KEY
from kc.users.models import CustomUser

from kc.api.v1.serializers.payments import ChargeSerializer



import stripe
import decimal


stripe.api_key = STRIPE_SECRET_KEY

# dictionary of prices : Stripe price ids
prices = {100 : 'price_1Hx3BUD3jYQzOC8Fcgg1oXuE', 120 : 'price_1Hx3CtD3jYQzOC8FAvKHU99k',
        140: 'price_1Hx3DKD3jYQzOC8FuyIDTgTL', 160 : 'price_1Hx3DcD3jYQzOC8Fc95dF6rH', 250 : 'price_1Hx3DqD3jYQzOC8F3wT1sBTW'}

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
            return Response({'Customer does not exist'}, status=status.HTTP_400_BAD_REQUEST)
      


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
        mail_list = request.data.get('mail_list')
        print('mail: ', mail_list)
        if mail_list == "true":
            mail_list = True
        else:
            mail_list = False
        # success = 'http://127.0.0.1:3000/payment-success'
        # cancel = 'http://127.0.0.1:3000/cancelled/'
        user.is_member = True
        success = 'https://www.kartclass.com/payment-success'
        cancel = 'https://www.kartclass.com/cancelled/'
        
        # Prevent user from buying category they already own
        if (category in user.category):
            return Response({'You already own this category'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.category.append(category)
        user.mail_list = mail_list
        user.save(update_fields=["category", "is_member", "mail_list"])

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
                # user.category.append(category)
                # user.save(update_fields=["category", "is_member"])
                return Response({'sessionId': checkout_session['id']},status=status.HTTP_202_ACCEPTED)
        
        # user.category.append(category)
        # user.save(update_fields=["category", "is_member"])
        return Response(status=status.HTTP_202_ACCEPTED)


