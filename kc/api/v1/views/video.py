from rest_framework import viewsets, generics, mixins, status
# from django.views.generic import ListView
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser
# from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
# from kc.api.common import exceptions
# import json
from kc.api.v1.serializers.video import *
from kc.api.v1.serializers.category import CategorySerializer
from kc.core.models import Video
# from braces.views import CsrfExemptMixin

from itertools import chain

class VideoListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,
                    # generics.GenericAPIView
                    ):
    # videos = [{i.title : i.category} for i in Video.objects.all()]
    # print(videos)
    

    # def to_dict(instance):
    #     opts = instance._meta
    #     data = {}
    #     for f in chain(opts.concrete_fields, opts.private_fields):
    #         data[f.name] = f.value_from_object(instance)
    #     for f in opts.many_to_many:
    #         data[f.name] = [i.id for i in f.value_from_object(instance)]
    #     return data

    serializer_class = VideoSerializer
    category = CategorySerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    lookup_field = 'slug'
    queryset = Video.objects.all()
    # videos = []
    # for i in Video.objects.all():
    #     videos.append(to_dict(i))

    # for v in videos:
        
        
    #     video = Video.objects.get(id=v['id'])
    #     cats = [c for c in v['category']]
    #     v['category'] = [cats_dict[x] for x in cats]
    #     v['category'] = dict.fromkeys(cats, "category")
       
        # serializer = VideoSerializer(video, data=v['category'], partial=True)
        # # v = Video()
        # # # print(serializer)
        # if serializer.is_valid():
        #     print('ok')
        #     serializer.save()
            
        # else:
        #     print(serializer.errors)
    # print(videos)
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
        categories = [i for i in data['category']]
        
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
      