from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration & Activation
    path('register/', views.register, name='register'),
    path('activate/<str:token>/', views.activate_account, name='activate'),
    
    # Login & Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Password Reset
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]