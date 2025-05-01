from celery import shared_task
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Client
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_trek_notifications_task():
    """Task to check for treks ending tomorrow and send notifications"""
    tomorrow = date.today() + timedelta(days=1)
    
    # Find clients with trekking or peak climbing ending tomorrow
    clients = Client.objects.filter(
        ending_date=tomorrow,
        notification_sent=False
    ).filter(
        trekking=True
    ) | Client.objects.filter(
        ending_date=tomorrow,
        notification_sent=False,
        peak_climbing=True
    )
    
    # Destination email from settings
    to_email = getattr(settings, 'TREK_NOTIFICATION_EMAIL', None)
    
    if not to_email:
        logger.error('TREK_NOTIFICATION_EMAIL not set in settings')
        return 'Error: No destination email provided'
        
    count = 0
    for client in clients:
        try:
            # Determine service type for better subject line
            service_type = "Trek"
            if client.peak_climbing:
                service_type = "Peak Climbing"
            
            # Better formatted subject
            subject = f"{service_type} Ending Tomorrow: {client.client_name} - {client.package}"
            
            # More detailed message with all relevant information
            message = f"""
Dear Team,

This is a reminder that the {service_type.lower()} for client {client.client_name} will be ending tomorrow.

CLIENT DETAILS:
- Name: {client.client_name}
- Email: {client.email}
- Country: {client.country}
- Phone: {client.phone_number}

SERVICE DETAILS:
- Package: {client.package}
- Guide: {client.guide}
- Porter: {client.porter}
- Starting Date: {client.starting_date}
- Ending Date: {client.ending_date}
- Total Days: {client.number_of_days}

PAYMENT STATUS: {client.payment_status.title()}

Please ensure all arrangements for their departure are in place.

This is an automated message from the Trek Management System.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            
            # Mark notification as sent
            client.notification_sent = True
            client.save(update_fields=['notification_sent'])
            count += 1
            
            logger.info(f'Successfully sent notification for {client.client_name} ({client.package})')
            
        except Exception as e:
            logger.error(f"Failed to send notification for client {client.id}: {str(e)}")
    
    result_message = f'Sent {count} notifications'
    logger.info(result_message)
    return result_message