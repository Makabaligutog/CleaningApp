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
from .forms import AdminSignupForm, AdminLoginForm
from .models import ServiceRating
from datetime import datetime
from calendar import month_name
from .models import Service
from django.core.files.storage import FileSystemStorage



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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
                return render(request, 'cleaning/register.html', {'form': form})

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
                return render(request, 'cleaning/register.html', {'form': form})

            # If validation passes, save the user and log them in
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to a relevant page (e.g., profile, home)
    else:
        form = RegisterForm()
    return render(request, 'cleaning/register.html', {'form': form})

# Booking Creation View
def create_booking(request):    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            # Get the service that the user is trying to book
            service = form.cleaned_data.get('service')  # Assuming 'service' is a field in your form

            # Check if the user has already booked this service
            if Booking.objects.filter(user=request.user, service=service).exists():
                messages.info(request, f"You have already booked the {service.name} service.")
                return redirect('cleaning/u-index.html')  # Redirect to the relevant page (e.g., user dashboard)
            
            # If no existing booking, create the new booking
            booking = form.save(commit=False)
            booking.user = request.user  # Assign the current user to the booking
            booking.save()

            # If the request is an AJAX request, return a JSON response
            if request.is_ajax():
                return JsonResponse({
                    "message": "Booking created successfully!",
                    "booking_id": str(booking.booking_id)
                }, status=201)

            # For non-AJAX requests, redirect the user
            messages.success(request, "Your booking has been successfully created!")
            return redirect('cleaning/u-index.html')  # Change to the relevant page after booking

        # If the form is not valid, return the user to the same page with errors
        return redirect('cleaning/u-index.html')  # Or render with the form and errors if needed
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
    success_url = reverse_lazy('user_profile')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Delete Booking View
@method_decorator(login_required, name='dispatch')
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'cleaning/booking_confirm_delete.html'
    success_url = reverse_lazy('user_profile')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


#user profile after mag book
def profile_view(request):
    # Fetch the user's latest booking, if any
    booking = Booking.objects.filter(user=request.user).last()  # Get the most recent booking
    return render(request, 'cleaning/user_profile.html', {'booking': booking})

#Admin dashboard

def admin_dashboard(request):
    bookings = Booking.objects.all() # Fetch all bookings for admin dashboard
    return render(request, 'cleaning/admin_dashboard.html', {'bookings': bookings})


def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status:
            booking.status = new_status
            booking.save()
            messages.success(request, 'Booking status updated successfully!')
        else:
            messages.error(request, 'Failed to update booking status. Please try again.')

        return redirect('ad_dashboard')

    return redirect('ad_dashboard')

# Admin Login View
def own_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_homepage')  # Redirect to the admin dashboard
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()

    return render(request, 'cleaning/admin_login.html', {'form': form})

# Admin Signup View
def own_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Admin account created successfully.')
                return redirect('admin_signup')  # Redirect to the admin dashboard or any other page
            else:
                messages.error(request, 'Signup failed. Please try again.')
    else:
        form = AdminSignupForm()
    
    return render(request, 'cleaning/admin_signup.html', {'form': form})

#cancel ang booking
def deny_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, 'Booking denied successfully!')
        
    return redirect('ad_dashboard')
#accept the booking
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == 'POST':
        booking.status = 'Accepted'
        booking.save()
        messages.success(request, 'Booking accepted successfully!')
        
    return redirect('ad_dashboard')


#services ratings
def save_ratings(request):
    if request.method == "POST":
        for service, _ in ServiceRating.SERVICE_CHOICES:
            for month in [
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ]:
                # Get the input value
                rating_key = f"ratings_{service}_{month}"
                rating_value = request.POST.get(rating_key)
                
                # If there's a value, proceed with save/update
                if rating_value:
                    rating_value = int(rating_value)  # Convert to integer
                    rating_obj, created = ServiceRating.objects.update_or_create(
                        service_name=service, 
                        month=month,
                        defaults={'rating': rating_value}
                    )
        # Redirect back to the ratings view
        return redirect('ratings')

    # If not POST, redirect to ratings page
    return redirect('ratings')

# Upload a services
def upload_service(request):
    if request.method == 'POST' and request.FILES['image']:
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']

        # Save the image and service data
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)

        new_service = Service(
            name=name,
            description=description,
            image=file_url
        )
        new_service.save()

        return redirect('ad_services')  # Redirect to services page

    return render(request, 'cleaning/admin_services.html')


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

#Anti bacterial in Services Learn More
def anti_bacterial(request):
    return render(request, 'cleaning/anti_bacterial.html')
# Admin ratings
def ratings_view(request):
    return render(request, 'cleaning/ratings.html')

# Admin services
def admin_services(request):
    services = Service.objects.all()
    return render(request, 'cleaning/admin_services.html', {'services': services})

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

#car interior
def car_interior(request):
    return render(request, 'cleaning/car_interior.html')

def deep_dry(request):
    return render(request, 'cleaning/deep_dry.html')

def deep_home(request):
    return render(request, 'cleaning/deep_home.html')

def deep_holstery(request):
    return render(request, 'cleaning/deep_holstery.html')


def sterilization(request):
    return render(request, 'cleaning/sterilization.html')

def residential_cleaning(request):
    return render(request, 'cleaning/residential.html')

def commercial_cleaning(request):
    return render(request, 'cleaning/commercial.html')

def move_in_cleaning(request):
    return render(request, 'cleaning/move_in.html')

def carpet_cleaning(request):
    return render(request, 'cleaning/carpet.html')

def window_cleaning(request):
    return render(request, 'cleaning/window.html')

#approved booking
def approved(request):
     # Fetch bookings data from the database
    all_bookings = Booking.objects.all()  # Replace with appropriate queryset if necessary
    approved_bookings = Booking.objects.filter(status='approved')
    pending_bookings = Booking.objects.filter(status='pending')

    # Calculate totals
    total_bookings = all_bookings.count()
    approved_count = approved_bookings.count()
    pending_count = pending_bookings.count()

    # Prepare context
    context = {
        'bookings': all_bookings,            # Use this for the table
        'approved_bookings': approved_count, # Count of approved bookings
        'pending_bookings': pending_count,   # Count of pending bookings
        'total_bookings': total_bookings     # Total bookings
    }
    return render(request, 'cleaning/approved.html', context)
def approve_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.status = Booking.CONFIRMED  # Update to approved status
        booking.save()
        return JsonResponse({'success': True, 'message': 'Booking approved successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def deny_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.status = Booking.DENIED  # Update to denied status
        booking.save()
        return JsonResponse({'success': True, 'message': 'Booking denied successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
