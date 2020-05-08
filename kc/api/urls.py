from django.urls import include, path

import api.v1.urls as v1_urls
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path('auth/token/', jwt_views.TokenObtainPairView.as_view(),
    #      name='auth-token-obtain-pair'),
    # path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
    #      name='auth-token-refresh'),
    path('v1/', include(v1_urls)),
]
