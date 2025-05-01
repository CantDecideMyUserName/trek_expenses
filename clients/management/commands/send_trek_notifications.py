import logging
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from clients.models import Client

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send email notifications for treks ending tomorrow'

    def handle(self, *args, **options):
        tomorrow = date.today() + timedelta(days=1)
        clients = Client.objects.filter(
            ending_date=tomorrow,
            notification_sent=False,
            trekking=True
        )
        
        count = 0
        for client in clients:
            try:
                subject = f"Trek Ending Tomorrow: {client.client_name}"
                message = f"""
                Dear Team,
                
                This is a reminder that the trek for client {client.client_name} will be ending tomorrow.
                
                Client Details:
                - Name: {client.client_name}
                - Trek/Package: {client.package}
                - Guide: {client.guide}
                - Starting Date: {client.starting_date}
                - Ending Date: {client.ending_date}
                
                Please ensure all arrangements for their departure are in place.
                
                Regards,
                Trek Management System
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.TREK_NOTIFICATION_EMAIL],
                    fail_silently=False,
                )
                
                client.notification_sent = True
                client.save(update_fields=['notification_sent'])
                count += 1
                
                self.stdout.write(self.style.SUCCESS(f'Successfully sent notification for {client.client_name}'))
            except Exception as e:
                logger.error(f"Failed to send notification for client {client.id}: {str(e)}")
                self.stdout.write(self.style.ERROR(f'Failed to send notification for {client.client_name}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Sent {count} notifications'))