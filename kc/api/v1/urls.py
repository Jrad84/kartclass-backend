from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from api.v1.views.article import ArticleView
from api.v1.views.testimonial import TestimonialView
from api.v1.views.video import VideoListView, VideoView
from api.v1.views.category import CategoryView
from api.v1.views.driver import DriverView
from api.v1.views.user import UserViewSet
from api.v1.views.me import MeView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
]

router = routers.DefaultRouter()
router.register(r'videos', VideoListView)
router.register(r'testimonials', TestimonialView)
router.register(r'categories', CategoryView)
router.register(r'articles', ArticleView)
router.register(r'drivers', DriverView)
router.register(r'user', UserViewSet)

urlpatterns.extend(router.urls)
# urlpatterns = [
#     path("", include(router.urls))
# ]
