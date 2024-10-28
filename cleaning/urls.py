from django.urls import path
from . import views
from .views import BookingUpdateView, BookingDeleteView, create_booking_views
from .views import add_review


from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about_home, name='home_about'),
    path('services/', views.services_home, name='home_services'),
    path('blog/', views.blog_home, name='home_blog'),

    # path('logout/', views.logout_view, name='logout'),
    path('user_homepage/', views.user_home, name='u_home'),
    path('user_service/', views.services, name='user_services'),
    path('user_about/', views.about, name='user_about'),
    path('user_blog/', views.blog, name='user_blog'),
    
    path('owner/', views.admin_home, name='admin_homepage'),
    path('admin_services/', views.admin_services, name='ad_services'),
    path('admin_about/', views.admin_about, name='ad_about'),
    path('admin_blog/', views.admin_blog, name='ad_blog'),
    path('admin_dashboard/', views.admin_dashboard, name='ad_dashboard'),
    
    path('profile/', views.profile_view, name='user_profile'),
    path('booking/update/<int:pk>/', BookingUpdateView.as_view(), name='update_booking'),
    path('booking/delete/<int:pk>/', BookingDeleteView.as_view(), name='delete_booking'),
    
    path('booking/create/', views.create_booking, name='create_booking'),  # New path for creating booking
    path('booking_create/views/', create_booking_views.as_view()),
    path('add_review/', views.add_review, name='add_review'),


]
