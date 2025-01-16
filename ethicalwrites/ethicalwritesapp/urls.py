"""
URL configuration for ethicalwrites project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from ethicalwritesapp import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),    
    path('signup', views.signup, name = "signup"),
    path('webpage1', views.webpage1, name= "webpage1"),
    path('webpage2', views.webpage2, name= "webpage2"),
    path('webpage3', views.webpage3, name= "webpage3"),
    path('webpage4', views.webpage4, name= "webpage4")
]
