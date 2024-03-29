from rest_framework import viewsets, generics, mixins, status
from kc.api.v1.serializers.article import ArticleSerializer
from rest_framework import permissions
from rest_framework.response import Response
from kc.core.models import Article

class ArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.AllowAny]


class ArticleUploadView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, pk):
        return Article.objects.get(pk=uid)

    def post(self, request):
        data=request.data
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
        article = self.get_object(pk=data['id'])
        serializer = ArticleSerializer(article, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data=request.data
        article = self.get_object(pk=data['id'])
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)