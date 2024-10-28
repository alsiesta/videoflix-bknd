# user/signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def set_user_inactive(sender, instance, created, **kwargs):
    logger.info(f"Signal triggered for user {instance.username}. Created: {created}")
    if created:
        logger.info(f"User {instance.username} created. Superuser: {instance.is_superuser}")
        if not instance.is_superuser:
            logger.info(f"Setting user {instance.username} to inactive.")
            instance.is_active = False
            instance.save(update_fields=['is_active'])
        else:
            logger.info(f"User {instance.username} is a superuser, not setting to inactive.")
    else:
        logger.info(f"User {instance.username} not created, not setting to inactive.")
