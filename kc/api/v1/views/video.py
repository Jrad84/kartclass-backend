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
# from kc.api.v1.serializers.tag import TagSerializer
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
    
    # serializer_class = VideoSerializer
    permission_classes = (permissions.AllowAny,)
    # parser_class = (FileUploadParser,)
    # queryset = ''

    def get_object(self, uid):
        return Category.objects.get(id=uid)

    def post(self, request):
        
        # categories = []
        # i = 0
        # while i < len(request.data['category']):
        #     categories.append(self.get_object(name=request.data['category'][i]))
        #     i+=1
        
        data=request.data
        # category = self.get_object(uid=data['category']['id'])
        # data['category'] = list(data['category'].items())
        
        # category = {
        #             'id': category.id,
        #             'name': category.name,
        #             'tier': category.tier,
        #             'description': category.description,
        #             'image': category.image,
        #             'amount': category.amount,
        #             'trailer': category.trailer
        #         }
        # data['category'] = category
        serializer = VideoSerializer(data=data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
       
        serializer.save()
        # v = json.dumps(video.__dict__)
        # print(v)
        # video.add(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        # uid = request.data['category']['id']
        # category = self.get_object(uid)
        # # serializer.category.set(category)
        # video = Video.create(validated_data=request.data)
        # if video:
        #     video.category.set(category)
        #     return Response(video, status=status.HTTP_200_OK)
       
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
        # video.category = category
        # video.save()
        # serializer.category = category
        # print(serializer)
        # for c in categories:
        #     cat = {}
        #     x = self.get_object(c.name)
        #     # cat['name'] = x.name
        #     cat['id'] = x.id
        #     # cat['amount'] = x.amount
        #     # cat['tier'] = x.tier
        #     # cat['description'] = x.description
        #     # cat['image'] = x.image
        #     # cat['trailer'] = x.trailer

        #     serializer.category = x.id
        #     print(serializer.category)
       
        

        # if serializer.is_valid():
           
        #     serializer.save()

        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

                   

   
   
