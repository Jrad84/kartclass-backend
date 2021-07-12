from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from kc.users.models import CustomUser

from kc.api.v1.serializers.payments import ChargeSerializer

class PaymentSuccessView(generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ''
    
        
    def post(self, request):
       
        # serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)
        temp = user.temp_cat
        # dont add a category more than once
        if temp not in user.category:
            user.category.append(temp)
      
        user.save(update_fields=["category"])
        return Response(status=status.HTTP_202_ACCEPTED)



