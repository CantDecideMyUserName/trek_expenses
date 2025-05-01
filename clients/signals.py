from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, date
from .models import Client

@receiver(post_save, sender=Client)
def check_notification_status(sender, instance, **kwargs):
    """
    When a client is saved, ensure notification_sent is set to False
    if the end date is in the future. This handles cases where a client's
    trip is extended or rescheduled.
    """
    # If ending date is changed and is in the future, reset notification flag
    if instance.ending_date > date.today():
        # Only reset if it was previously set to True
        if instance.notification_sent:
            instance.notification_sent = False
            # Use update_fields to avoid triggering post_save recursively
            instance.save(update_fields=['notification_sent'])