from django.urls import path
from .views import reset_password, register

urlpatterns = [
	path('reset_password/', reset_password, name='reset_password'),
	path('register/', register, name='register')
]