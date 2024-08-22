from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import Video, Category, Favorite
from .forms import ImageUploadForm
import os

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'path', 'imagepath')
    actions = ['upload_image']

    def upload_image(self, request, queryset):
        if 'apply' in request.POST:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data['image']
                for video in queryset:
                    # Save the image to the desired location
                    image_path = os.path.join('media/images', image.name)
                    with open(image_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    # Update the imagepath field
                    video.imagepath = image_path
                    video.image_file = image  # Save the image file
                    video.save()
                self.message_user(request, "Image uploaded and path set successfully.")
                return redirect(request.get_full_path())
        else:
            form = ImageUploadForm()

        return render(request, 'admin/upload_image.html', {'form': form, 'videos': queryset})

    upload_image.short_description = "Upload image and set imagepath"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-image/', self.admin_site.admin_view(self.upload_image), name='upload_image'),
        ]
        return custom_urls + urls

admin.site.register(Video, VideoAdmin)
admin.site.register(Category)
admin.site.register(Favorite)