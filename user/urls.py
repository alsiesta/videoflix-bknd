from django.urls import include, path
from .views import user_reset_password, register, mail_reset_password, password_reset_confirm
from user import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
	path('user_reset_password/', user_reset_password, name='reset_password'),
	path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
	path('mail_reset_password/', mail_reset_password, name='mail_reset_password'),
	path('register/', register, name='register')
]