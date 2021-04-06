from rest_framework import viewsets, generics, filters, mixins, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from kc.api.v1.serializers.blog import BlogSerializer
from kc.core.models import Blog

class BlogListView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet,
                    ):

    serializer_class = BlogSerializer
    # authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    
    queryset = Blog.objects.all()

class BlogUploadView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, pk):
        return Blog.objects.get(pk=pk)

    def post(self, request):
        data=request.data
        serializer = BlogSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
      
        blog = self.get_object(pk=data['id'])
       
        serializer = BlogSerializer(blog, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data=request.data
        blog = self.get_object(pk=data['id'])
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)