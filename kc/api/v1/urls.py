
from django.urls import path, include
from kc.api.v1.views.purchased import PurchasedDatePostView, PurchasedDateView
from kc.api.v1.views.worksheet import WorksheetView
from kc.core.models import PurchasedDate
from rest_framework import routers
from kc.api.v1.views.testimonial import TestimonialView
from kc.api.v1.views.video import *
from kc.api.v1.views.podcast import *
from kc.api.v1.views.category import CategoryView
from rest_framework_simplejwt import views as jwt_views
from kc.api.v1.views.token import MyTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views
from kc.api.v1.views.user import *
from kc.api.v1.views.article import *
from kc.api.v1.views.worksheet import *
from django.views.decorators.csrf import csrf_exempt
from kc.api.v1.views.me import *
# from kc.api.v1.views.facebook import FacebookSocialAuthView
# from kc.api.v1.views.social import FacebookLoginView
from kc.api.v1.views.payments import *
from kc.api.v1.views.mail_list import MailListView
from kc.api.v1.views.product import *
from kc.api.v1.views.blog import *

urlpatterns = [
    #  path('auth/facebook/', FacebookSocialAuthView.as_view(), name='auth'),
     # path('auth/oauth/', include('rest_framework_social_oauth2.urls')),
#    path("oauth/login/", SocialLoginView.as_view(), name="fb_login"),
     # path("auth/social/facebook/", FacebookLoginView.as_view(), name="fb_login"),
    #  path('auth/token/', csrf_exempt(MyTokenObtainPairView.as_view()),
    #      name='auth-token-obtain-pair'),
    #  path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
    #      name='auth-token-refresh'),
    #  path('auth/token/verify', jwt_views.TokenVerifyView.as_view(),
    #       name='auth-token-verify'),
     path('auth/logout/', LogoutView.as_view(), name='logout'),
     path('me/', MeView.as_view(), name='me'),   
     path('edit-password/', ChangePasswordView.as_view(), name='edit-password'),
     path('edit-email/', ChangeEmailView.as_view(), name='edit-email'),
     path('like-video/', VideoLikeView.as_view(), name='like-video'),
     path('unlike-video/', VideoUnLikeView.as_view(), name='unlike-video'),
     path('watch-video/', VideoWatchView.as_view(), name='watch-video'),
     path('like-podcast/', PodcastLikeView.as_view(), name='like-podcast'),
     path('unlike-podcast/', PodcastUnLikeView.as_view(), name='unlike-podcast'),
     path('listen-podcast/', PodcastListenView.as_view(), name='listen-podcast'),
     path('like-article/', VideoLikeView.as_view(), name='like-article'),
     path('unlike-article/', VideoUnLikeView.as_view(), name='unlike-article'),
     path('checkout/', ChargeListView.as_view(), name='checkout'),
     path('upload-video/', csrf_exempt(VideoUploadView.as_view()), name='upload-video'),
     path('upload-article/', csrf_exempt(ArticleUploadView.as_view()), name='upload-article'),
     path('upload-worksheet/', csrf_exempt(WorksheetUploadView.as_view()), name='upload-worksheet'),
     path('upload-product/', csrf_exempt(ProductUploadView.as_view()), name='upload-product'),
     path('request-reset-email/', RequestPasswordResetView.as_view(),
         name="request-reset-email"),
     path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
     path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
     path('mail-list/', MailListView.as_view(), name='mail-list'),
     path('upload-blog/', csrf_exempt(BlogUploadView.as_view()), name='upload-blog'),
     path('pay-success/', PaymentSuccessView.as_view(), name='pay-success'),
     path('popup/', PopupView.as_view(), name='popup'),
     path('post-purchasedDate/', PurchasedDatePostView.as_view(), name='post-purchasedDate'),
     
]

router = routers.DefaultRouter()
router.register(r'videos', VideoListView)
router.register(r'podcasts', PodcastListView)
router.register(r'blogs', BlogListView)
router.register(r'testimonials', TestimonialView)
router.register(r'categories', CategoryView)
router.register(r'articles', ArticleView)
router.register(r'register', UserViewSet)
router.register(r'edit-user', UpdateUserView, basename='edit-user')
router.register(r'products', ProductListView)
router.register(r'worksheets', WorksheetView)
router.register(r'purchasedDate', PurchasedDateView)


urlpatterns.extend(router.urls)

