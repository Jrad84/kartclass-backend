from rest_framework import viewsets, generics, filters, mixins, status
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from kc.api.common import exceptions
import json
from kc.api.v1.serializers.video import *
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Video, Category
from braces.views import CsrfExemptMixin

class VideoListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,
                    # generics.GenericAPIView
                    ):

    serializer_class = VideoSerializer
    category = CategorySerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    
    queryset = Video.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'category__id')

   
    @csrf_exempt
    def patch(self, request):
        # uid = request.data['id']
        
        vid_id = request.data['id']
        video = Video.objects.get(id=vid_id)
        
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            video.likes += 1
            serializer.save()
            return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VideoLikeView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    # viewsets.GenericViewSet,
                    generics.GenericAPIView
                    ):
    
    def get_object(self, pk):
        return Video.objects.get(pk=pk)
   
    @csrf_exempt
    def patch(self, request):
        
        vid_id = request.data['id']
        video = self.get_object(pk=vid_id)
        
        serializer = VideoLikeSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUnLikeView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView
                    ):
    
    def get_object(self, pk):
        return Video.objects.get(pk=pk)
   
    @csrf_exempt
    def patch(self, request):
       
        vid_id = request.data['id']
        video = self.get_object(pk=vid_id)
        
        serializer = VideoUnLikeSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoUploadView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, uid):
        return Video.objects.get(id=uid)

    def post(self, request):
        data=request.data
        serializer = VideoSerializer(data=data)
        print(serializer)
        categories = [i for i in data['category']]
        print(categories)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
      
        video = self.get_object(uid=data['id'])
        serializer = VideoSerializer(video, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      