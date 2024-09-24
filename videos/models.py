from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.conf import settings
import os

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    image_file = models.FileField(upload_to='images', blank=True, null=True)  # New field for image
    categories = models.ManyToManyField(Category, related_name='videos')
    path = models.CharField(max_length=255, blank=True, null=True)
    imagepath = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.video_file:
            # Extract the file name without extension
            base_name = os.path.splitext(os.path.basename(self.video_file.name))[0]
            # Extract the file extension
            extension = os.path.splitext(self.video_file.name)[1]
            # Generate the path
            # self.path = f"media/videos/{base_name}{extension}"
            self.path = f"media/videos/{base_name}.m3u8"
        
        if self.image_file:
            # Extract the file name without extension
            base_name = os.path.splitext(os.path.basename(self.image_file.name))[0]
            # Extract the file extension
            extension = os.path.splitext(self.image_file.name)[1]
            # Generate the image path
            self.imagepath = f"media/images/{base_name}{extension}"
        
        super(Video, self).save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"