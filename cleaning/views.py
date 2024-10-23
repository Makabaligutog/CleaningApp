from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib import messages

def home(request):
    return render(request, 'cleaning/index.html')

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in and redirect to a success page
            login(request, user)
            return redirect('u_home')
        else:
            # If login fails, use Django's messages framework
            messages.error(request, 'Invalid username or password')
            return render(request, 'cleaning/login.html')    

    # If GET request or login fails, render the login page
    return render(request, 'cleaning/login.html')
    # if request.method == 'POST':
    #     # Get the username and password from the form
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
        
    #     # Authenticate the user
    #     user = authenticate(request, username=username, password=password)
        
    #     if user is not None:
    #         # Log the user in and redirect to a success page
    #         login(request, user)
    #         return redirect('home')
    #     else:
    #         # If the login is unsuccessful, add an error message
    #         context = {'error_message': 'Invalid username or password'}
    #         return render(request, 'cleaning/login.html', context)    
    # return render(request, 'cleaning/login.html')

# registration
def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
        form = RegisterForm()

    return render(request, 'cleaning/register.html', {'form': form})


#logout
def logout_view(request):
    logout(request)
    return redirect('login')

#User homepage
def Userhomepage(request):
        return render(request, 'cleaning/u-index.html')
