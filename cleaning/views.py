from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

# registration
def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Create and save the user
            user = User.objects.create_user(username=email, email=email, password=password)
            
            # Log the user in automatically after registration
            login(request, user)
            
            # Redirect to a success page (e.g., home)
            messages.success(request, 'Registration successful.')
            return redirect('home')  # Redirect to the home page or another URL
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
