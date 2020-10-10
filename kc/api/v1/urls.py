from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from kc.api.v1.views.article import ArticleView
from kc.api.v1.views.testimonial import TestimonialView
from kc.api.v1.views.video import *
from kc.api.v1.views.category import CategoryView
from kc.api.v1.views.driver import DriverView
from rest_framework_simplejwt import views as jwt_views
from kc.api.v1.views.user import *
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.views.me import *
from kc.api.v1.views.payments import *


urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(),
         name='auth-token-obtain-pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='auth-token-refresh'),
    path('auth/token/verify', jwt_views.TokenVerifyView.as_view(),
          name='auth-token-verify'),
    path('auth/logout/', LogoutView, name='logout'),
    path('me/', MeView.as_view(), name='me'),   
    path('edit-password/', ChangePasswordView.as_view(), name='edit-password'),
    path('edit-email/', ChangeEmailView.as_view(), name='edit-email'),
    path('current-user/', CurrentCustomerDetailView.as_view(), name='stripe-current-customer-detail'),
    path('create-subscription/', SubscriptionView.as_view(), name='stripe-subscription'),
    path('change-card/', ChangeCardView.as_view(), name='stripe-change-card'),
    path('charges/', ChargeListView.as_view(), name='stripe-charges'),
    path('plans/', PlanListView.as_view(), name='stripe-plans'),
    path('webhook/', CancelView.as_view(), name='stripe-cancel'),
    path('customer/',CurrentCustomerDetailView.as_view(), name='stripe-customer'),
    path('create-customer/', CurrentCustomerDetailView.as_view(), name='create-stripe-customer'),
    path('like-video/', VideoLikeView.as_view(), name='like-video'),
    path('unlike-video/', VideoUnLikeView.as_view(), name='unlike-video'),
    path('checkout/', ChargeListView.as_view(), name='checkout'),
    path('upload-video/', csrf_exempt(VideoUploadView.as_view()), name='upload-video'),
    
   
     
]

router = routers.DefaultRouter()
router.register(r'videos', VideoListView)
router.register(r'testimonials', TestimonialView)
router.register(r'categories', CategoryView)
router.register(r'articles', ArticleView)
router.register(r'drivers', DriverView)
router.register(r'accounts', UserViewSet)
router.register(r'edit-user', UpdateUserView, basename='edit-user')




urlpatterns.extend(router.urls)

