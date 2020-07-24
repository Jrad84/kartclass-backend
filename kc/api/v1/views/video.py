from rest_framework import viewsets, generics, filters, mixins
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from api.common import exceptions
from api.v1.serializers.video import VideoSerializer
from api.v1.serializers.category import CategorySerializer
from core.models import Video, Category

class VideoView(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):

    serializer_class = VideoSerializer
    queryset = Video.objects.all()


class VideoListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,
                    # generics.GenericAPIView
                    ):
    # User permission to access videos
    # def get_user(request):
    #     return request.user

    # user = self.get_user()
    serializer_class = VideoSerializer
    category = CategorySerializer
    permission_classes = [permissions.IsAdminUser, permissions.AllowAny,]
    # categories = Category.objects.all()
    # queryset = Video.objects.filter(category <= user.category)
    queryset = Video.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'category__id')

