import logging
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from clients.models import Client

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send email notifications for treks and climbing trips ending tomorrow'

    def add_arguments(self, parser):
        # Optional email argument to override settings
        parser.add_argument(
            '--email',
            dest='email',
            help='Email address to send notifications to (overrides settings)',
        )

    def handle(self, *args, **options):
        tomorrow = date.today() + timedelta(days=1)
        
        # Find clients with trekking or peak climbing ending tomorrow
        clients = Client.objects.filter(
            ending_date=tomorrow,
            notification_sent=False
        ).filter(
            # Match either trekking OR peak climbing
            trekking=True
        ) | Client.objects.filter(
            ending_date=tomorrow,
            notification_sent=False,
            peak_climbing=True
        )
        
        # Destination email - from argument or settings
        to_email = options.get('email') or getattr(settings, 'TREK_NOTIFICATION_EMAIL', None)
        
        if not to_email:
            self.stderr.write(self.style.ERROR(
                'No destination email provided. Set TREK_NOTIFICATION_EMAIL in settings or use --email'
            ))
            return
            
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
                
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully sent notification for {client.client_name} ({client.package})'
                ))
            except Exception as e:
                logger.error(f"Failed to send notification for client {client.id}: {str(e)}")
                self.stdout.write(self.style.ERROR(
                    f'Failed to send notification for {client.client_name}: {str(e)}'
                ))
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Sent {count} notifications'))
        else:
            self.stdout.write(self.style.WARNING('No clients found with trips ending tomorrow'))