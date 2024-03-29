from rest_framework import status, generics, permissions
from rest_framework.response import Response
from kc.users.models import CustomUser
from kc.api.v1.serializers.payments import ChargeSerializer
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


FREE = 6 # id of Free Category
SPROKETS = 12 # id of Junior Sprokets Category
NKA = 13 # id of NKA Category


class ChargeListView(generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ''
   
    def post(self, request):
       
        user = CustomUser.objects.get(email=request.user)
      
        # only if checkout required
        if request.data.get('temp') is not None:
            user.temp_cat = request.data.get('temp')
            user.checkout = request.data.get('checkout')

        mail_list = request.data.get('mail_list')
        
       
        if mail_list == "true":
            mail_list = True
        else:
            mail_list = False

        user.mail_list = mail_list
        user.is_member = True

        if request.data.get('sprokets') == 1 and SPROKETS not in user.category:
            user.category.append(SPROKETS)

        if request.data.get('sprokets') == 2 and NKA not in user.category:
            user.category.append(NKA)

        if FREE not in user.category:
            user.category.append(FREE)
       
        user.save(update_fields=["checkout", "category", "temp_cat", "is_member", "mail_list"])

        return Response(status=status.HTTP_202_ACCEPTED)

class PaymentSuccessView(generics.ListAPIView):
    """ Add category to user model after successful payment """
    serializer_class = ChargeSerializer
    queryset = ''
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        user = CustomUser.objects.get(email=request.user)
        
        if user.temp_cat is not None:
            if user.temp_cat == 8:
                user.purchasedChampions = datetime.now()
                user.save(update_fields=["purchasedChampions"])

            if user.temp_cat not in user.category:
                user.category.append(user.temp_cat)
                user.temp_cat = None
                user.checkout = None
                user.save(update_fields=["category", "temp_cat", "checkout"])

                return Response({'temp_cat': user.temp_cat, 'category': user.category}, status=status.HTTP_200_OK)
        

        error = "Failed to update category"
                
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
      
       
  