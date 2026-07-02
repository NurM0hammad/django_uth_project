from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_verified', 'created_at', 'updated_at']
    list_filter = ['email_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'location', 'birth_date')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Verification', {
            'fields': ('email_verified', 'verification_token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )