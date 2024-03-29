from rest_framework import viewsets, generics, mixins, status, permissions

from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.serializers.video import *
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Video
import logging

logger = logging.getLogger(__name__)



class VideoListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,
                  
                    ):
 

    serializer_class = VideoSerializer
    category = CategorySerializer
    
    permission_classes = [permissions.AllowAny,]
    lookup_field = 'slug'
    queryset = Video.objects.all()
  
    @csrf_exempt
    def patch(self, request):
       
        vid_id = request.data['id']
        video = Video.objects.get(id=vid_id)
        serializer = VideoSerializer(video, data=request.data, partial=True)
       

        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VideoLikeView(mixins.ListModelMixin,
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


class VideoWatchView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView
                    ):
    
    serializer_class = VideoViewSerializer

    def get_object(self, pk):
        return Video.objects.get(pk=pk)
   
    @csrf_exempt
    def patch(self, request):
        
        vid_id = request.data['id']
        video = self.get_object(pk=vid_id)
        
        serializer = VideoViewSerializer(video, data=request.data, partial=True)
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

    def get_object(self, pk):
        return Video.objects.get(pk=pk)

    def post(self, request):
        data=request.data
        serializer = VideoSerializer(data=data)
       
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
      
        video = self.get_object(pk=data['id'])
       
        serializer = VideoSerializer(video, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data=request.data
        video = self.get_object(pk=data['id'])
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      