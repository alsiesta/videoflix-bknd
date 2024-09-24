# user/signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def set_user_inactive(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        logger.info(f"Setting user {instance.username} to inactive.")
        instance.is_active = False
        instance.save(update_fields=['is_active'])