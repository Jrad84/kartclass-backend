from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from kc.users.models import CustomUser

from kc.api.v1.serializers.payments import ChargeSerializer

class PaymentSuccessView(generics.ListAPIView):
    """ List customer charges """
    serializer_class = ChargeSerializer
    queryset = ''
    
        
    def post(self, request):
       
        serializer = self.serializer_class(data=request.data)
        user = CustomUser.objects.get(email=request.user)
        temp = user.temp_cat
        if temp not in user.category:
            user.category.append(temp)
      
        user.save(update_fields=["category"])
        return Response(status=status.HTTP_202_ACCEPTED)



