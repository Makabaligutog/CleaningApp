from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from .models import Booking
from .forms import RegisterForm, BookingForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Home view
def home(request):
    return render(request, 'cleaning/index.html')

# User Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('u_home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'cleaning/login.html')

# User Registration View
def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Automatically saves the user
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful.')
            return redirect('u_home')  # Redirect to home after signup
    else:
        form = RegisterForm()

    return render(request, 'cleaning/register.html', {'form': form})

#booking na
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Associate the booking with the logged-in user
            booking.save()
            return JsonResponse({"message": "Booking created successfully!"}, status=201)

        # If form is invalid, return the specific errors
        return JsonResponse({"error": form.errors}, status=400)

    # Return error for methods other than POST
    return JsonResponse({"error": "Invalid request method."}, status=405)

# User Profile View
@login_required
def profile_view(request):
    try:
        booking = Booking.objects.get(user=request.user)
    except Booking.DoesNotExist:
        booking = None  # Handle case where no booking exists
    return render(request, 'cleaning/user_profile.html', {'booking': booking})

# Update Booking View
@method_decorator(login_required, name='dispatch')
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_update.html'
    success_url = reverse_lazy('profile_view')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Delete Booking View
@method_decorator(login_required, name='dispatch')
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('profile_view')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# User Homepage
def user_home(request):
    return render(request, 'cleaning/u-index.html')

# User Services Page
def services(request):
    return render(request, 'cleaning/u-services.html')

# User About Us Page
def about(request):
    return render(request, 'cleaning/u-about.html')

# User Blog Page
def blog(request):
    return render(request, 'cleaning/u-blog.html')

# Admin Views
def admin_home(request):
    return render(request, 'cleaning/admin_index.html')

def admin_services(request):
    return render(request, 'cleaning/admin_services.html')

def admin_about(request):
    return render(request, 'cleaning/admin_about.html')

def admin_blog(request):
    return render(request, 'cleaning/admin_blog.html')

# About Home Page
def about_home(request):
    return render(request, 'cleaning/about.html')

# Services Home Page
def services_home(request):
    return render(request, 'cleaning/services.html')

# Blog Home Page
def blog_home(request):
    return render(request, 'cleaning/blog.html')
