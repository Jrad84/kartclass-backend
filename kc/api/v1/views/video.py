from rest_framework import viewsets, generics, filters, mixins, status
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from kc.api.common import exceptions
from kc.api.v1.serializers.video import *
from kc.api.v1.serializers.category import CategorySerializer
from kc.api.v1.serializers.tag import TagSerializer
from kc.core.models import Video, Category, Tag
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
        print(request.data)
        # uid = request.data['id']
        
        vid_id = request.data['id']
        video = Video.objects.get(id=vid_id)
        
        serializer = VideoSerializer(video, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        video.likes += 1
        
        serializer.save()
        return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)
        

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
        serializer.is_valid(raise_exception=True)
  
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        serializer.is_valid(raise_exception=True)

        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class VideoUploadView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    serializer_class = VideoUploadSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = ''

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)

                   

   
   
