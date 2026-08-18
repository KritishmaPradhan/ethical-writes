from django.contrib import admin
from ethicalwritesapp.models import UserInfo, UserWork, WorkComment, WorkLike

class AdminDisplay(admin.ModelAdmin):
    Admin_display = ('username', 'password', 'email', 'phone', 'continent') 
admin.site.register(UserInfo, AdminDisplay)
admin.site.register(UserWork)
admin.site.register(WorkComment)
admin.site.register(WorkLike)
