from videos.tasks import convert_to_480p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os 

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video has been saved', instance)
    if created:
        print('New video has been created')
        convert_to_480p(instance.video_file.path)
    

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('Video has been deleted')

    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
