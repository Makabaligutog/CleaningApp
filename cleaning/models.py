# models.py

from django.db import models
from django.contrib.auth.models import User
import uuid  # Required for UUIDField

class Booking(models.Model):
    # Custom primary key using UUID
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    CLEANING_CHOICES = [
        ('residential', 'Residential Cleaning'),
        ('commercial', 'Commercial Cleaning'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning_service = models.CharField(max_length=20, choices=CLEANING_CHOICES)
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.full_name} - {self.cleaning_service}"
