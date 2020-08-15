from rest_framework import viewsets
from kc.api.v1.serializers.article import ArticleSerializer
from rest_framework import permissions
from kc.core.models import Article

class ArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.AllowAny]