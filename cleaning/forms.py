from django import forms
from django.contrib.auth.models import User
from .models import Booking
from .models import ServiceReview
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ServiceReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceReview
        fields = ['customer_name', 'message', 'photo', 'rating']
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'user', 'cleaning_service', 'first_name', 'last_name', 'contact_number',
            'address', 'additional_info', 'status', 'booking_date'
        ]
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['status']
     
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class AdminSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
