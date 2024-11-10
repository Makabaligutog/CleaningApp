from django.contrib import admin
from .models import Booking
from .forms import BookingForm

class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_id', 'user', 'cleaning_service', 'first_name', 'last_name',
        'contact_number', 'address', 'additional_info', 'status', 'booking_date'
    ]
    list_filter = ['status', 'booking_date']  # Optional, for filtering by status and date
    form = BookingForm

admin.site.register(Booking, BookingAdmin)
