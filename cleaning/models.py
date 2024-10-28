# models.py

from django.db import models
from django.contrib.auth.models import User
import uuid  # Required for UUIDField
from django.db import models

#mao ni ang admin site sa Blog na mag upload 
class ServiceReview(models.Model):
    customer_name = models.CharField(max_length=100)
    message = models.TextField()
    photo = models.ImageField(upload_to='service_photos/')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Ratings from 1 to 5

    def __str__(self):
        return self.customer_name


class Booking(models.Model):
    # Custom primary key using UUID
    booking_id = models.AutoField(primary_key=True, editable=False)
    
    CLEANING_CHOICES = [
    ('residential', 'Residential Cleaning'),
    ('commercial', 'Commercial Cleaning'),
    ('deep-cleaning', 'Deep Cleaning'),
    ('move-in-out', 'Move-in/Move-out Cleaning'),
    ('carpet-cleaning', 'Carpet Cleaning'),
    ('upholstery-cleaning', 'Upholstery Cleaning'),
    ('window-cleaning', 'Window Cleaning'),
    ('eco-friendly', 'Eco-friendly Green Cleaning'),
    
    ]

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning_service = models.CharField(max_length=20, choices=CLEANING_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default='Unknown')
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.first_name} {self.last_name} - {self.cleaning_service}"

