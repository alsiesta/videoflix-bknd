from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import index, register_user, activate_account, resend_activation_link, custom_logout, password_change_view, PasswordResetRequestView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('', index, name='index'),
    path('videos/', include('videos.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('accounts/register/', register_user, name='register'),
    path('accounts/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),  
    path('accounts/password_change/', password_change_view, name='password_change'),
    
    # # this are the default auth urls
    # accounts/ login/ [name='login']
    # accounts/ logout/ [name='logout']
    # accounts/ password_change/ [name='password_change']
    # accounts/ password_change/done/ [name='password_change_done']
    # accounts/ password_reset/ [name='password_reset']
    # accounts/ password_reset/done/ [name='password_reset_done']
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/ reset/done/ [name='password_reset_complete']
    # accounts/register/ [name='register']
    
    path('logout/', custom_logout, name='logout'),    
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('resend_activation_link/', resend_activation_link, name='resend_activation_link'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
