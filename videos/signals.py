import glob
from videos.tasks import convert_to_480p, convert_to_720p, convert_to_1080p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os 
import django_rq
# from lib2to3.pytree import convert
# import queue

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video has been saved', instance)
    if created:
        print('New video has been created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_to_480p, instance.video_file.path)
        queue.enqueue(convert_to_720p, instance.video_file.path)
        queue.enqueue(convert_to_1080p, instance.video_file.path)
    

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('Video has been deleted')

    if instance.video_file:
        base_path = instance.video_file.path
        base_dir = os.path.dirname(base_path)
        base_name = os.path.splitext(os.path.basename(base_path))[0]

        # Delete the original video file
        if os.path.isfile(base_path):
            os.remove(base_path)

        # Delete all related .m3u8 and .ts files
        patterns = [
            f"{base_name}_*.m3u8",
            f"{base_name}_*.ts"
        ]

        for pattern in patterns:
            for file_path in glob.glob(os.path.join(base_dir, pattern)):
                if os.path.isfile(file_path):
                    os.remove(file_path)