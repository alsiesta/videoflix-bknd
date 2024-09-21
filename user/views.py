from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, EmailMultiAlternatives



from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from .serializers import PasswordResetSerializer, RegistrationSerializer, UserSerializer, GroupSerializer, EmailPasswordResetSerializer, NewPasswordResetSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, edited, updated or deleted.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
#  User can reset password when being logged in
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_reset_password(request):
    serializer = PasswordResetSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        print("PasswordResetSerializer")
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User sends email to reset password
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def mail_reset_password(request):
    serializer = EmailPasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name_html = "user/password_reset_email.html"
                email_template_name_txt = "user/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': settings.FRONTEND_HOST,
                    'site_name': 'Your Videoflix',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email_html = render_to_string(email_template_name_html, c)
                email_txt = render_to_string(email_template_name_txt, c)
                
                email_message = EmailMultiAlternatives(subject, email_txt, settings.DEFAULT_FROM_EMAIL, [user.email])
                email_message.attach_alternative(email_html, "text/html")
                email_message.send(fail_silently=False)
                
            return Response({"detail": "Password reset email has been sent to " + user.email}, status=status.HTTP_200_OK)
        return Response({"detail": "No user is associated with this email address."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        serializer = NewPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate token and verification URL
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f"{settings.FRONTEND_HOST}/verify-email/{uid}/{token}/"
        
        # Prepare email content
        subject = "Registration Successful"
        email_template_name_html = "user/registration_success_email.html"
        email_template_name_txt = "user/registration_success_email.txt"
        context = {
            "username": user.username,
            "email": user.email,
            'domain': settings.FRONTEND_HOST,
            'site_name': 'Your Videoflix',
            'verification_url': verification_url,  # Include the verification URL in the context

        }
        email_html = render_to_string(email_template_name_html, context)
        email_txt = render_to_string(email_template_name_txt, context)
        
        # Send email
        email_message = EmailMultiAlternatives(subject, email_txt, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_message.attach_alternative(email_html, "text/html")
        email_message.send(fail_silently=False)
        
        return Response({
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        return Response({"detail": "Email verified successfully. Your account is now active."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)