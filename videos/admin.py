from django.contrib import admin
from .models import Video, Category, Favorite


admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Favorite)