from rest_framework import generics, mixins, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from kc.api.v1.serializers.mail_list import MailListSerializer
from kc.core.models import MailList
from django.http import JsonResponse

class MailListView(generics.GenericAPIView, 
                    mixins.ListModelMixin, 
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = MailListSerializer
    permission_classes = [permissions.AllowAny,]
    
    @csrf_exempt
    def post(self, request):
        
        serializer = MailListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        permission_classes = [permissions.IsAdminUser,]
        mail_list = MailList.objects.all().values()
        return JsonResponse({"mail_list": list(mail_list)})
        