from rest_framework import viewsets, generics, mixins, status
from rest_framework import permissions
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.serializers.podcast import *
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Podcast
import logging

logger = logging.getLogger(__name__)



class PodcastListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,
                  
                    ):
 

    serializer_class = PodcastSerializer
    category = CategorySerializer
    
    permission_classes = [permissions.AllowAny,]
    lookup_field = 'slug'
    queryset = Podcast.objects.all()
  
    @csrf_exempt
    def patch(self, request):
       
        pod_id = request.data['id']
        podcast = Podcast.objects.get(id=pod_id)
        serializer = PodcastSerializer(podcast, data=request.data, partial=True)
       

        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Update details successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PodcastLikeView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView
                    ):
    
    def get_object(self, pk):
        return Podcast.objects.get(pk=pk)
   
    @csrf_exempt
    def patch(self, request):
        
        podcast_id = request.data['id']
        podcast = self.get_object(pk=podcast_id)
        
        serializer = PodcastLikeSerializer(podcast, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
           
            return Response(serializer.data, status=status.HTTP_200_OK)
      
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PodcastUnLikeView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView
                    ):
    
    def get_object(self, pk):
        return Podcast.objects.get(pk=pk)
   
    @csrf_exempt
    def patch(self, request):
       
        podcast_id = request.data['id']
        podcast = self.get_object(pk=podcast_id)
        
        serializer = PodcastUnLikeSerializer(podcast, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PodcastListenView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView
                    ):
    
    def get_object(self, pk):
        return Podcast.objects.get(pk=pk)
   
    @csrf_exempt
    def patch(self, request):
        
        podcast_id = request.data['id']
        podcast = self.get_object(pk=podcast_id)
        
        serializer = PodcastListenSerializer(podcast, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
           
            return Response(serializer.data, status=status.HTTP_200_OK)
      
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class PodcastUploadView(mixins.ListModelMixin,
#                     mixins.RetrieveModelMixin,
#                     mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):

#     permission_classes = (permissions.IsAdminUser,)

#     def get_object(self, pk):
#         return Podcast.objects.get(pk=pk)

#     def post(self, request):
#         data=request.data
#         serializer = PodcastSerializer(data=data)
       
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request):
#         data=request.data
      
#         podcast = self.get_object(pk=data['id'])
       
#         serializer = PodcastSerializer(podcast, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request):
#         data=request.data
#         podcast = self.get_object(pk=data['id'])
#         podcast.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
      