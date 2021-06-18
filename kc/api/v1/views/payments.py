from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from kc.settings.base import API_VERSION, SHOPIFY_URL, SHOPIFY_PASSWORD
from kc.users.models import CustomUser
import shopify
from kc.api.v1.serializers.payments import ChargeSerializer



FREE = '6641681006801' # id of Free Category
BEGINNER = '6641680679121'
CLUB = '6641680679121'
NATIONAL = '6641682219217'
REGIONAL = '6641681531089'
STATE = '6641681989841'


class ChargeListView(generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    queryset = ''
    
        
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)
        jared = CustomUser.objects.get(email='jaredtaback.com')
        ben = CustomUser.objects.get(email='bmouritz@me.com')
        dave = CustomUser.objects.get(email='davidsera@live.com.au')

        jared.category = []
        ben.category = []
        dave.category = []
        jared.save()
        ben.save()
        dave.save()
        # print(jared.category[0])
        # jared.category.append(FREE, BEGINNER, CLUB, REGIONAL, STATE, NATIONAL)
        # ben.category.append(FREE, BEGINNER, CLUB, REGIONAL, STATE, NATIONAL)
        # dave.category.append(FREE, BEGINNER, CLUB, REGIONAL, STATE, NATIONAL)
        jared.save()
        ben.save()
        dave.save()
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
        success = 'http://127.0.0.1:3000/payment-success'
        # cancel = 'http://127.0.0.1:3000/cancelled/'
      
        # If first time checkout, add Free category
        if FREE not in user.category:
            user.category.append(FREE)

        user.save(update_fields=["category", "temp_cat", "is_member", "mail_list"])

        if amount > 0:
            try:
                session = shopify.Session(SHOPIFY_URL, API_VERSION, SHOPIFY_PASSWORD)
                
                shopify.ShopifyResource.activate_session(session)
                shopify.ApplicationCharge.create({
                    'name': 'Kart Class',
                    'price': amount,
                    'test': True,
                    'return_url': success

                })
                
                shopify.ShopifyResource.clear_session()
                return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
        print('line 70')
        return Response(status=status.HTTP_202_ACCEPTED)


