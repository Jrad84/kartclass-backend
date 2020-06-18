from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from api.v1.views.article import ArticleView
from api.v1.views.testimonial import TestimonialView
from api.v1.views.video import VideoListView, VideoView
from api.v1.views.category import CategoryView
from api.v1.views.driver import DriverView
from rest_framework_simplejwt import views as jwt_views
from api.v1.views.user import UserViewSet
from api.v1.views.me import MeView


urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(),
         name='auth-token-obtain-pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='auth-token-refresh'),
    path('me/', MeView.as_view(), name='me'),   
     path('accounts/', include('rest_registration.api.urls')),
]

router = routers.DefaultRouter()
router.register(r'videos', VideoListView)
router.register(r'testimonials', TestimonialView)
router.register(r'categories', CategoryView)
router.register(r'articles', ArticleView)
router.register(r'drivers', DriverView)
# router.register(r'accounts', UserViewSet)


urlpatterns.extend(router.urls)

