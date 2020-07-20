from rest_framework import viewsets
from api.v1.serializers.article import ArticleSerializer
from rest_framework import permissions
from core.models import Article

class ArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.AllowAny]