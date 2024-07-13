from django.contrib import admin
from django.urls import path, include
from . views import index, register_user, activate_account
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/register/', register_user, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('accounts/', include('django.contrib.auth.urls') ),
]
