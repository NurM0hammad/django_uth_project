from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.db.models import Q
import hashlib
import datetime

from .forms import (
    RegistrationForm, UserLoginForm, UserProfileForm, 
    CustomPasswordChangeForm, PasswordResetRequestForm, SetPasswordForm
)
from .models import UserProfile
from .utils import generate_verification_token, send_verification_email

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # User must verify email
            user.save()
            
            # Create user profile
            profile = UserProfile.objects.create(user=user)
            
            # Generate verification token
            token = generate_verification_token(user)
            profile.verification_token = token
            profile.save()
            
            # Send verification email
            send_verification_email(user, token, request)
            
            messages.success(request, 
                'Registration successful! Please check your email to verify your account.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def activate_account(request, token):
    try:
        profile = UserProfile.objects.get(verification_token=token)
        user = profile.user
        
        if user.is_active:
            messages.info(request, 'Your account is already verified.')
            return redirect('accounts:login')
        
        # Activate user
        user.is_active = True
        user.save()
        profile.email_verified = True
        profile.verification_token = None
        profile.save()
        
        messages.success(request, 'Your account has been successfully verified! You can now login.')
        return redirect('accounts:login')
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid verification token.')
        return redirect('accounts:login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    next_url = request.GET.get('next', 'accounts:profile')
                    return redirect(next_url)
                else:
                    messages.warning(request, 'Your account is not verified. Please check your email.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Check if profile picture is being uploaded
            if 'profile_picture' in request.FILES:
                # Delete old picture if it's not default
                if profile.profile_picture and profile.profile_picture.name != 'profile_pics/default.jpg':
                    profile.profile_picture.delete(save=False)
            
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            
            if users.exists():
                user = users.first()
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset link
                reset_link = request.build_absolute_uri(
                    reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Send email
                subject = 'Password Reset Request'
                message = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                    'site_name': 'My Django Site',
                })
                
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                
                messages.success(request, 
                    'We have sent you an email with instructions to reset your password.')
                return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, 'Your password has been reset successfully. You can now login.')
                return redirect('accounts:login')
        else:
            form = SetPasswordForm()
        
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('accounts:password_reset')