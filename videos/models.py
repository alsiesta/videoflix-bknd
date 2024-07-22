from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#create a class for the model with created_at, title, description, video_file
class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='videos')

    def __str__(self):
        return self.title
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"