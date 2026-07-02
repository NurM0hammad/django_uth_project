from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default='profile_pics/default.jpg',
        null=True,
        blank=True
    )
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize profile picture
        if self.profile_picture and self.profile_picture.name != 'profile_pics/default.jpg':
            img_path = self.profile_picture.path
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(img_path)
                except Exception as e:
                    print(f"Error resizing image: {e}")

    def delete(self, *args, **kwargs):
        # Delete profile picture when user is deleted
        if self.profile_picture and self.profile_picture.name != 'profile_pics/default.jpg':
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        super().delete(*args, **kwargs)