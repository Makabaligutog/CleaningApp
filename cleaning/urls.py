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
    path('profile/', views.profile_view, name='user_profile'),
    path('AntiBacterialMistTreatment/', views.anti_bacterial, name='anti_bacterial'),
    path('CarInteriorDetailing/', views.car_interior, name='car_interior'),
    path('DeepDryCleaning/', views.deep_dry, name='deep_dry'),
    path('DeepHomeCleaning/', views.deep_home, name='deep_home'),
    path('DeepUpholsteryShampooing/', views.deep_holstery, name='deep_holstery'),
    path('SuperiorSteamSterilization/', views.sterilization, name='sterilize'),
    path('ResidentialCleaning/', views.residential_cleaning, name='residential_cleaning'),
    path('CommercialCleaning/', views.commercial_cleaning, name='commercial_cleaning'),
    path('MoveInMoveOutCleaning/', views.move_in_cleaning, name='move_in_out'),
    path('CarpetCleaning/', views.carpet_cleaning, name='carpet_cleaning'),
    path('WindowCleaning/', views.window_cleaning, name='window_cleaning'),
    
    
    

    
    # Admin URLs
    path('owner/', views.admin_home, name='admin_homepage'),
    path('admin_services/', views.admin_services, name='ad_services'),
    path('admin_about/', views.admin_about, name='ad_about'),
    path('admin_blog/', views.admin_blog, name='ad_blog'),
    path('admin_dashboard/', views.admin_dashboard, name='ad_dashboard'),
    path('ratings/', views.ratings_view, name='ratings'),
    path('save_ratings/', views.save_ratings, name='save_ratings'),
    path('upload-service/', views.upload_service, name='upload_service'),

    
    path('booking/update/<int:pk>/', BookingUpdateView.as_view(), name='update_booking'),
    path('booking/delete/<int:pk>/', BookingDeleteView.as_view(), name='delete_booking'),
    path('booking/create/', views.create_booking, name='create_booking'),  # New path for creating booking
    path('booking_create/views/', create_booking_views.as_view()),
    path('add_review/', views.add_review, name='add_review'),
    path('ApprovedBooking/', views.approved, name='ad_approved'),
    # admin book
    # path('admin/booking/update/<int:booking_id>/', views.update_booking_status, name='admin_update_booking'),
    path('update-booking-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),

    #approved page
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('deny-booking/<int:booking_id>/', views.deny_booking, name='deny_booking'),

    
    # admin login and signup
    path('owner/signup/', views.own_signup, name='owner_signup'),
    path('owner/login/', views.own_login, name='owner_login'),
    
    #action
    path('deny-booking/<int:booking_id>/', views.deny_booking, name='deny_booking'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
