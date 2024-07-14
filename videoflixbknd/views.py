"""
Views for user registration and account activation.
"""
import json
import os
from pathlib import Path
from django.conf import settings

from dotenv import load_dotenv

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from verify_email.email_handler import send_verification_email

from .forms import RegistrationForm
from .tokens import account_activation_token

def get_base_url():
    if settings.DEBUG:
        return settings.DEV_HOST
    else:
        return settings.PROD_HOST
    
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
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Your account has been successfully activated.', 'username': user.username, 'password': 'YourPasswordHere'})
    else:
        return JsonResponse({'status': 'error', 'message': 'The activation link is invalid or expired.'}, status=400)
    

from django.views.decorators.csrf import csrf_exempt

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
            baseUrl = data.get('baseUrl')
            activation_link = f"{baseUrl}/activate/{uidb64}/{token}/"
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

