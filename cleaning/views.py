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
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseForbidden
from .forms import ServiceReviewForm

from django.views import View
#admin blog sa katong mag upload
from .models import ServiceReview

def blog(request):
    reviews = ServiceReview.objects.all()
    return render(request, 'cleaning/Admin_blog.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        form = ServiceReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ad_blog')  # Redirect to the blog page or any other page
    else:
        form = ServiceReviewForm()
    
    return render(request, 'cleaning/Admin_blog.html', {'form': form})
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
            return redirect('signup') 
    else:
        form = RegisterForm()

    return render(request, 'cleaning/register.html', {'form': form})

# Booking Creation View
@login_required
@csrf_protect
def create_booking(request):    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=True)
            booking.user = request.user
            booking.save()

            if request.is_ajax():
                return JsonResponse({
                    "message": "Booking created successfully!",
                    "booking_id": str(booking.booking_id)
                }, status=201)

            return redirect(request, 'cleaning/u-index.html')
        
        return redirect(request, 'cleaning/u-index.html')

class create_booking_views(View):
    def post(self, request):
        print('creating booking')
        try:
            form = BookingForm(request.POST)
            print(request.POST)
            if form.is_valid():
                newbooking = form.save(commit=False)
                newbooking.user = request.user
                newbooking.save()
                return JsonResponse({'success': "Successfuly saved Booking"}, status = 200)
            else:
                print(form.errors)
                return JsonResponse({'error': "Form invalid"}, status = 405)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)
        
# User Profile View
@login_required
def profile_view(request):
    booking = Booking.objects.filter(user=request.user).first()
    return render(request, 'cleaning/user_profile.html', {'booking': booking})

# Update Booking View
@method_decorator(login_required, name='dispatch')
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'cleaning/booking_update.html'
    success_url = reverse_lazy('profile_view')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Delete Booking View
@method_decorator(login_required, name='dispatch')
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'cleaning/booking_confirm_delete.html'
    success_url = reverse_lazy('profile_view')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


#user profile after mag book
def profile_view(request):
    # Fetch the user's latest booking, if any
    booking = Booking.objects.filter(user=request.user).last()  # Get the most recent booking
    return render(request, 'cleaning/user_profile.html', {'booking': booking})


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

# Admin homepage
@login_required
def admin_home(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    bookings = Booking.objects.all()
    return render(request, 'cleaning/Admin_index.html', {'bookings': bookings})

# Admin dashboard view
@login_required
def admin_dashboard(request):
    return render(request, 'cleaning/admin_dashboard.html')

# Admin services
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
