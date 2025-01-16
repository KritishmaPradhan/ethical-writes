from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length= 30)
    password = models.CharField(max_length= 30)
    email = models.CharField(max_length= 30)
    phone = models.CharField(max_length= 13)
    continent = models.CharField(max_length= 15)
