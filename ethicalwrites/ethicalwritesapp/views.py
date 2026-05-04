from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from ethicalwritesapp.models import UserInfo


def index(request):
    """Homepage view - accessible to all."""
    return render(request, 'index.html')


@require_http_methods(["GET", "POST"])
def login_user(request):
    """Handle user login with authentication."""
    # Redirect already logged-in users
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('webpage1')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'login_user.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('webpage1')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login_user.html')


@require_http_methods(["GET", "POST"])
def signup(request):
    """Handle user registration with validation."""
    # Redirect already logged-in users
    if request.user.is_authenticated:
        messages.info(request, "You are already registered.")
        return redirect('webpage1')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        phone = request.POST.get('phone', '').strip()
        continent = request.POST.get('continent', '').strip()
        
        # Validate input
        if not all([username, email, password]):
            messages.error(request, "Username, email, and password are required.")
            return render(request, 'signup.html')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'signup.html')
        
        try:
            # Create Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create UserInfo profile
            UserInfo.objects.create(
                user=user,
                phone=phone,
                continent=continent
            )
            
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login_user')
        
        except IntegrityError:
            messages.error(request, "Username or email already exists. Please choose different credentials.")
            return render(request, 'signup.html')
        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')


@login_required(login_url='login_user')
@require_http_methods(["GET"])
def logout_user(request):
    """Handle user logout - requires authentication."""
    username = request.user.username
    logout(request)
    messages.success(request, f"Successfully logged out, {username}. See you soon!")
    return redirect('home')


@login_required(login_url='login_user')
@require_http_methods(["GET"])
def webpage1(request):
    """Protected page 1 - requires authentication."""
    return render(request, 'webpage1.html')


@login_required(login_url='login_user')
@require_http_methods(["GET"])
def webpage2(request):
    """Protected page 2 - requires authentication."""
    return render(request, 'webpage2.html')


@login_required(login_url='login_user')
@require_http_methods(["GET"])
def webpage3(request):
    """Protected page 3 - requires authentication."""
    return render(request, 'webpage3.html')


@login_required(login_url='login_user')
@require_http_methods(["GET"])
def webpage4(request):
    """Protected page 4 - requires authentication."""
    return render(request, 'webpage4.html')