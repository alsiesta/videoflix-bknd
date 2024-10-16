from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import LoginView, index, register_user, activate_account, resend_activation_link, custom_logout, password_change_view, PasswordResetRequestView, reset_password_form


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('videos/', include('videos.urls')),
    path('user/', include('user.urls')),    
    path('logout/', custom_logout, name='logout'),    
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('resend_activation_link/', resend_activation_link, name='resend_activation_link'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('django-rq/', include('django_rq.urls')),
]+ debug_toolbar_urls() + staticfiles_urlpatterns()


if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
