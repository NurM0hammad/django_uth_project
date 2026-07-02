from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import ContactMessage, NewsletterSubscriber, SiteSetting, TeamMember
from .forms import ContactForm, NewsletterForm
import json

class HomeView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)[:4]
        context['newsletter_form'] = NewsletterForm()
        
        # Get dynamic stats
        context['stats'] = {
            'users': 5000,
            'projects': 1200,
            'satisfaction': '99%',
            'uptime': '24/7'
        }
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            messages.success(request, 'Successfully subscribed to our newsletter!')
            
            # Send welcome email
            try:
                send_mail(
                    'Welcome to Our Newsletter',
                    'Thank you for subscribing to our newsletter. You\'ll receive updates and news.',
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=True,
                )
            except:
                pass
            
            return redirect('pages:home')
        else:
            messages.error(request, 'Please enter a valid email address.')
            return self.render_to_response(self.get_context_data(newsletter_form=form))

class AboutView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        context['mission'] = SiteSetting.objects.filter(key='mission_statement').first()
        context['vision'] = SiteSetting.objects.filter(key='vision_statement').first()
        return context

class ContactView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        
        # Get contact info from settings
        context['contact_info'] = {
            'address': SiteSetting.objects.filter(key='address').first(),
            'phone': SiteSetting.objects.filter(key='phone').first(),
            'email': SiteSetting.objects.filter(key='contact_email').first(),
        }
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            try:
                send_mail(
                    f'New Contact Message: {contact.subject}',
                    f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
                    contact.email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Your message has been sent successfully! We\'ll get back to you soon.')
            return redirect('pages:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
            return self.render_to_response(self.get_context_data(form=form))

class LocationView(TemplateView):
    template_name = 'pages/location.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get location settings
        context['location'] = {
            'address': SiteSetting.objects.filter(key='address').first(),
            'phone': SiteSetting.objects.filter(key='phone').first(),
            'email': SiteSetting.objects.filter(key='contact_email').first(),
            'latitude': SiteSetting.objects.filter(key='latitude').first(),
            'longitude': SiteSetting.objects.filter(key='longitude').first(),
            'working_hours': SiteSetting.objects.filter(key='working_hours').first(),
        }
        
        return context

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'pages/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages_count'] = ContactMessage.objects.filter(is_read=False).count()
        context['subscribers_count'] = NewsletterSubscriber.objects.filter(is_active=True).count()
        context['recent_messages'] = ContactMessage.objects.all()[:5]
        return context