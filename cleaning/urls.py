from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    # path('logout/', views.logout_view, name='logout'),
    path('user_homepage/', views.user_home, name='u_home'),
    path('user_service/', views.services, name='services'),
    path('user_about/', views.about, name='about'),
    path('user_blog/', views.blog, name='blog'),
    path('admin_homepage', views.admin_home, name='admin_home'),
    path('admin_services', views.admin_services, name='admin_services'),
    path('admin_about', views.admin_about, name='admin_about'),
    path('admin_blog', views.admin_blog, name='admin_blog'),
    
   
]
