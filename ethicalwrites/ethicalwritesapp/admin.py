from django.contrib import admin
from ethicalwritesapp.models import UserInfo

class AdminDisplay(admin.ModelAdmin):
    Admin_display = ('username', 'password', 'email', 'phone', 'continent') 
admin.site.register(UserInfo, AdminDisplay)
