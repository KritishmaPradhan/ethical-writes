from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    """Extended user profile linked to Django's User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=13, blank=True, null=True)
    continent = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name_plural = 'User Info'
