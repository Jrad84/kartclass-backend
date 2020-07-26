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
from api.v1.views.registration import RegistrationView
from api.v1.views.me import MeView
from api.v1.views.payments import *


urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(),
         name='auth-token-obtain-pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='auth-token-refresh'),
    path('me/', MeView.as_view(), name='me'),   
     # path('accounts/', include('rest_registration.api.urls')),
     path('current-user/', CurrentCustomerDetailView.as_view(), name='stripe-current-customer-detail'),
    path('create-subscription/', SubscriptionView.as_view(), name='stripe-subscription'),
    path('change-card/', ChangeCardView.as_view(), name='stripe-change-card'),
    path('charges/', ChargeListView.as_view(), name='stripe-charges'),
    path('invoices/', InvoiceListView.as_view(), name='stripe-invoices'),
    path('plans/', PlanListView.as_view(), name='stripe-plans'),
    path('events/', EventListView.as_view(), name='stripe-events'),
    path('webhook/', CancelView.as_view(), name='stripe-cancel'),
    path('customer/',CurrentCustomerDetailView.as_view(), name='stripe-customer'),
    path('create-customer/', CurrentCustomerDetailView.as_view(), name='create-stripe-customer'),
    
]

router = routers.DefaultRouter()
router.register(r'videos', VideoListView)
router.register(r'testimonials', TestimonialView)
router.register(r'categories', CategoryView)
router.register(r'articles', ArticleView)
router.register(r'drivers', DriverView)
router.register(r'accounts', UserViewSet)
router.register(r'registration', RegistrationView)



urlpatterns.extend(router.urls)

