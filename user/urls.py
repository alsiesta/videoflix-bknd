from django.urls import include, path
from .views import user_reset_password, register, mail_reset_password
from user import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
	path('user_reset_password/', user_reset_password, name='reset_password'),
	path('mail_reset_password/', mail_reset_password, name='mail_reset_password'),
	path('register/', register, name='register')
]