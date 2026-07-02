from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from accounts.models import UserProfile

def generate_verification_token(user):
    """Generate a unique verification token for the user."""
    return get_random_string(length=64)

def send_verification_email(user, token, request):
    """Send verification email to user."""
    # Get the current site
    current_site = get_current_site(request)
    domain = current_site.domain
    
    verification_link = f'http://{domain}/accounts/activate/{token}/'
    
    subject = 'Verify Your Email Address'
    message = render_to_string('accounts/verification_email.html', {
        'user': user,
        'verification_link': verification_link,
        'site_name': current_site.name,
        'domain': domain,
    })
    
    send_mail(
        subject, 
        message, 
        settings.DEFAULT_FROM_EMAIL, 
        [user.email],
        fail_silently=False,
    )

def create_user_profile(sender, instance, created, **kwargs):
    """Create profile for new user."""
    if created:
        UserProfile.objects.create(user=instance)