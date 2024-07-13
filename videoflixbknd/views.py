"""
Views for user registration and account activation.
"""
import json

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
            baseUrl = form.data.get('baseUrl')
            activation_link = f"{baseUrl}/activate/{uidb64}/{token}/"
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


    
        return JsonResponse({'status': 'success', 'message': 'Your account has been successfully activated.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'The activation link is invalid or expired.'}, status=400)
    
