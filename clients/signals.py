from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, date
from .models import Client

@receiver(post_save, sender=Client)
def schedule_end_notification(sender, instance, created, **kwargs):
    """Schedule notification for one day before trek ends"""
    # This will be called when a client is saved, but we'll handle the actual sending in a management command
    pass

# Create a management command to run daily via cron job