from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . views import index, register_user, activate_account, resend_activation_link
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/register/', register_user, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('resend_activation_link/', resend_activation_link, name='resend_activation_link'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
