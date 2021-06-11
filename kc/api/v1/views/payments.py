from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from kc.settings.base import STRIPE_SECRET_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from kc.users.models import CustomUser

from kc.api.v1.serializers.payments import ChargeSerializer



import stripe
import decimal


stripe.api_key = STRIPE_SECRET_KEY
FREE = 6641681006801 # id of Free Category

# dictionary of prices : Stripe price ids
prices = {100 : 'price_1Hx4ZRD3jYQzOC8F5IXHCnF8', 120 : 'price_1Hx4ZjD3jYQzOC8FKkNLq03l',
        140: 'price_1Hx4a6D3jYQzOC8FmF4KO6MF', 160 : 'price_1Hx4aRD3jYQzOC8FsDbO8j59', 250 : 'price_1Hx4agD3jYQzOC8FEchQeJXj'}

# class StripeView(APIView):
#     """ Generic API StripeView """
#     permission_classes = (permissions.IsAuthenticated, )

#     def get_current_subscription(self):
#         try:
#             return self.request.user.customer.subscription
#         except Subscription.DoesNotExist:
#             return None

#     def get_customer(self):
#         try:
#             return self.request.user.customer
#         except ObjectDoesNotExist:
#             return Response({'Customer does not exist'}, status=status.HTTP_400_BAD_REQUEST)
      


class ChargeListView(generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    queryset = ''
    
        
    def post(self, request):
       
        serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)

        amount = float(request.data.get('price'))
        # if amount > 0:
        #     price = prices[amount / 100]
        user.temp_cat = request.data.get('category')

        mail_list = request.data.get('mail_list')
       
        if mail_list == "true":
            mail_list = True
        else:
            mail_list = False

        user.mail_list = mail_list
        user.is_member = True
        # success = 'http://127.0.0.1:3000/payment-success'
        # cancel = 'http://127.0.0.1:3000/cancelled/'
        success = 'https://www.kartclass.com/payment-success'
        cancel = 'https://www.kartclass.com/cancelled/'

        # If first time checkout, add Free category
        if FREE not in user.category:
            user.category.append(FREE)

        user.save(update_fields=["category", "temp_cat", "is_member", "mail_list"])

        # if amount > 0:
        #     checkout_session = stripe.checkout.Session.create(
        #                     payment_method_types = ['card'],
        #                     mode='payment',
        #                     line_items = [{
        #                         'price': amount,
        #                         'quantity': 1
        #                     }],
        #                     success_url = success,
        #                     cancel_url = cancel
        #         )

        #     if (checkout_session):
        #         return Response({'sessionId': checkout_session['id']},status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_202_ACCEPTED)


