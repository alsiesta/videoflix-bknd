"""
Views for user registration and account activation.
"""
import json
import os
from pathlib import Path
from unittest.mock import DEFAULT
from django.conf import settings
from urllib.parse import urlencode



from dotenv import load_dotenv

from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


from .serializers import PasswordResetRequestSerializer

from verify_email.email_handler import send_verification_email

from .forms import RegistrationForm
from .tokens import account_activation_token

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'is_active': user.is_active,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


@require_http_methods(["GET"])
def custom_logout(request):
    logout(request)
    return redirect('index')

def get_base_url():
    if settings.DEBUG:
        return settings.DEV_HOST
    else:
        return settings.PROD_HOST
    
@login_required
def password_change_view(request):
    return render(request, 'registration/password_change_form.html')

@login_required
@cache_page(CACHE_TTL)
def index(request):
    """
    Display the index page with any messages.
    """
    messages_to_display = messages.get_messages(request)
    return render(request, "index.html", {"messages": messages_to_display})

@csrf_exempt
def register_user(request):
    """
    Handle user registration and send account activation email.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        form = RegistrationForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            # protocol = 'https' if request.is_secure() else 'http'
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            base_url = get_base_url()
            activation_link = f"{base_url}/activate/{uidb64}/{token}/"
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return JsonResponse({'message': 'Account created successfully. Please check your email to activate your account.'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


def activate_account(request, uidb64, token):
    """
    Activate user account if the provided token is valid.
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user) not needed here as the login is done in the frontend
        response_data = {
            'status': 'success',
            'username': user.username,
            'message': 'You activated your account successfully. You can now sign in.',
        }
    else:
        response_data = {
            'status': 'error',
        }
    query_string = urlencode(response_data)
    redirect_url = f'http://localhost:4200/login?{query_string}'
    return HttpResponseRedirect(redirect_url)
    


@csrf_exempt
def resend_activation_link(request):
    """
    Resend activation link if the user requests it.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)
            
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist'}, status=404)

            if user.is_active:
                return JsonResponse({'message': 'Account is already active'}, status=400)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # baseUrl = data.get('baseUrl') Funktioniert nicht
            activation_link = f"http://127.0.0.1:8000/activate/{uidb64}/{token}/"
            mail_subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return JsonResponse({'message': 'Activation link has been resent. Please check your email.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/accounts/reset/{uid}/{token}/')
                context = {
                    'user': user,
                    'reset_link': reset_link,
                }
                subject = 'Password Reset Request'
                message = render_to_string('registration/password_reset_email.html', context)
                send_mail(subject, message, 'no-reply@videoflix.com', [user.email])
                return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
