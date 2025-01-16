from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from ethicalwritesapp.models import UserInfo
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')
def login_user(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        my_user = authenticate(request, username = u_name, password = pass_word)
        if my_user is not None:
            login(request,my_user)
            messages.success(request, "Successfully logged in")
            return redirect('webpage1') 
        else:
            messages.error(request, "Incorrect credentials")
            return redirect('login_user') 
    return render(request, 'login_user.html')
def signup(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        emai_l = request.POST.get('email')
        phonee = request.POST.get('phone')
        c_ontinent = request.POST.get('continent')
        my_user1 = User.objects.create_user(username= u_name, email = emai_l, password = pass_word)
        my_user1.save()
        my_user = UserInfo(username=u_name, password = pass_word, email = emai_l, phone = phonee, continent = c_ontinent)
        my_user.save()
        messages.success(request, "Account created successfully")
        return redirect('login_user') 
    return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def webpage1(request):
    return render(request, 'webpage1.html')
def webpage2(request):
    return render(request, 'webpage2.html')
def webpage3(request):
    return render(request, 'webpage3.html')
def webpage4(request):
    return render(request, 'webpage4.html')