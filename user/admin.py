from django.contrib import admin
from user.models import CustomUser
from user.forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (
            'Additional Info',
            {
                'fields': (
                    'story',
                    'phone',
                    'address',
                ),
            },
        ),
        *UserAdmin.fieldsets,
    )
