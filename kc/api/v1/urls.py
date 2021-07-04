
from django.urls import path, include
from rest_framework import routers
from kc.api.v1.views.testimonial import TestimonialView
from kc.api.v1.views.video import *
from kc.api.v1.views.category import CategoryView
from kc.api.v1.views.pay_success import PaymentSuccessView
from rest_framework_simplejwt import views as jwt_views
from kc.api.v1.views.token import MyTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views
from kc.api.v1.views.user import *
from kc.api.v1.views.article import *
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.views.me import *
from kc.api.v1.views.payments import *
from kc.api.v1.views.mail_list import MailListView
from kc.api.v1.views.product import *
from kc.api.v1.views.blog import *

urlpatterns = [
    
     # path('auth/', include('djoser.urls')),
     # path('auth/', include('djoser.urls.authtoken')),
     # path('auth/', include('djoser.urls.jwt')),
   path('auth/token/', csrf_exempt(MyTokenObtainPairView.as_view()),
         name='auth-token-obtain-pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='auth-token-refresh'),
    path('auth/token/verify', jwt_views.TokenVerifyView.as_view(),
          name='auth-token-verify'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),   
    path('edit-password/', ChangePasswordView.as_view(), name='edit-password'),
    path('edit-email/', ChangeEmailView.as_view(), name='edit-email'),
    path('like-video/', VideoLikeView.as_view(), name='like-video'),
    path('unlike-video/', VideoUnLikeView.as_view(), name='unlike-video'),
     path('like-article/', VideoLikeView.as_view(), name='like-article'),
    path('unlike-article/', VideoUnLikeView.as_view(), name='unlike-article'),
    path('checkout/', ChargeListView.as_view(), name='checkout'),
    path('upload-video/', csrf_exempt(VideoUploadView.as_view()), name='upload-video'),
    path('upload-article/', csrf_exempt(ArticleUploadView.as_view()), name='upload-article'),
      path('upload-product/', csrf_exempt(ProductUploadView.as_view()), name='upload-product'),
    path('request-reset-email/', RequestPasswordResetView.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
     path('mail-list/', MailListView.as_view(), name='mail-list'),
     path('upload-blog/', csrf_exempt(BlogUploadView.as_view()), name='upload-blog'),
     path('pay-success/', PaymentSuccessView.as_view(), name='pay-success')

]

router = routers.DefaultRouter()
router.register(r'videos', VideoListView)
router.register(r'blogs', BlogListView)
router.register(r'testimonials', TestimonialView)
router.register(r'categories', CategoryView)
router.register(r'categories', CategoryView)
router.register(r'articles', ArticleView)
router.register(r'accounts', UserViewSet)
router.register(r'edit-user', UpdateUserView, basename='edit-user')
router.register(r'products', ProductListView)





urlpatterns.extend(router.urls)

