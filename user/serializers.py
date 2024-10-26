from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model

# created a custom user model which extends the AbstractUser model so it has to be imported first
User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
        
class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("Old password is incorrect.")
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
class EmailPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class NewPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=2)

    def validate_new_password(self, value):
        # Add any custom validation for the new password here
        return value
    

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'story', 'phone', 'address']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            story=validated_data.get('story', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        return user