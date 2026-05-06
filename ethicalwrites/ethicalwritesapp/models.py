from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    """Extended user profile linked to Django's User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    continent = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile" if self.user else "Profile"

    class Meta:
        verbose_name_plural = 'User Info'


class UserWork(models.Model):
    """Model to store user's freewriting submissions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='works')
    username = models.CharField(max_length=150)
    submitted_date = models.DateTimeField(auto_now_add=True)
    freewriting = models.TextField()
    author = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.submitted_date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = 'User Works'
        ordering = ['-submitted_date']
