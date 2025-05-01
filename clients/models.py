from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

class Client(models.Model):
    # Basic Information
    client_name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    passport = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    quick_notes = models.TextField(blank=True)
    
    # Service Dates
    starting_date = models.DateField()
    ending_date = models.DateField()
    total_days = models.IntegerField(help_text="Total days of service")
    
    # Services Offered (using checkboxes in the form)
    trekking = models.BooleanField(default=False)
    peak_climbing = models.BooleanField(default=False)
    tour = models.BooleanField(default=False)
    adventure_day_activities = models.BooleanField(default=False)
    flight = models.BooleanField(default=False)
    misc_service = models.CharField(max_length=100, blank=True)
    
    # For trekking and peak climbing
    guide = models.CharField(max_length=100, blank=True)
    porter = models.CharField(max_length=100, blank=True)
    package = models.CharField(max_length=100, blank=True)
    transport = models.CharField(max_length=100, blank=True)
    accommodation = models.CharField(max_length=100, blank=True)
    trekking_days = models.IntegerField(null=True, blank=True, 
                                      help_text="Number of actual trekking/climbing days")
    
    # For other services
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('completed', 'Completed')
    ], default='pending')
    
    # Email notification status
    notification_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.client_name
    
    @property
    def trek_name(self):
        return self.package if self.trekking or self.peak_climbing else ""
        
    @property
    def number_of_days(self):
        """For backwards compatibility with existing code"""
        return self.total_days
    
    class Meta:
        ordering = ['starting_date']


class PriceItem(models.Model):
    client = models.ForeignKey(Client, related_name='price_items', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.description} - {self.amount}"