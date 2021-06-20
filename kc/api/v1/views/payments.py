# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth import get_user_model
# from django.utils.encoding import smart_str
# from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.response import Response
from kc.users.models import CustomUser
from kc.api.v1.serializers.payments import ChargeSerializer



FREE = 1 # id of Free Category
BEGINNER = 2
CLUB = 3
NATIONAL = 6
REGIONAL = 4
STATE = 5

cats = {FREE, BEGINNER, CLUB, NATIONAL, REGIONAL, STATE}
class ChargeListView(generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    queryset = ''
    
    def post(self, request):
        
        # serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)
    
        # amount = float(request.data.get('price'))
        # if amount > 0:
        #     price = prices[amount / 100]
        user.temp_cat = request.data.get('temp')

        mail_list = request.data.get('mail_list')
       
        if mail_list == "true":
            mail_list = True
        else:
            mail_list = False

        user.mail_list = mail_list
        user.is_member = True
       
        # If first time checkout, add Free category
        if FREE not in user.category:
            user.category.append(FREE)

        user.save(update_fields=["category", "temp_cat", "is_member", "mail_list"])

        return Response(status=status.HTTP_202_ACCEPTED)

class PaymentSuccessView(generics.ListAPIView):
    """ Add category to user model after successful payment """
    serializer_class = ChargeSerializer
    queryset = ''

    def post(self, request):
        
        # serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)
        user.category.append(user.temp_cat)
        user.temp_cat = None
        user.save(update_fields=["category", "temp_cat"])
      
        return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)
  