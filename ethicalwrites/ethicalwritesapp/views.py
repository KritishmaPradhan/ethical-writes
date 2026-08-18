from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods

from ethicalwritesapp.models import UserInfo, UserWork, WorkComment, WorkLike


def index(request):
    """Homepage view - accessible to all."""
    return render(request, 'index.html')


@require_http_methods(["GET", "POST"])
def login_user(request):
    """Handle user login with authentication."""
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
        messages.error(request, "Invalid username or password.")

    return render(request, 'login_user.html')


@require_http_methods(["GET", "POST"])
def signup(request):
    """Handle user registration with validation."""
    if request.user.is_authenticated:
        messages.info(request, "You are already registered.")
        return redirect('webpage1')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        phone = request.POST.get('phone', '').strip()
        continent = request.POST.get('continent', '').strip()

        if not all([username, email, password]):
            messages.error(request, "Username, email, and password are required.")
            return render(request, 'signup.html')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'signup.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

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
        except Exception:
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
@require_http_methods(["GET", "POST"])
def webpage1(request):
    """Protected page 1 - requires authentication. Handles work submission and displays user works."""
    if request.method == 'POST':
        freewriting = request.POST.get('freewriting', '').strip()
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()

        if not freewriting:
            messages.error(request, "Please enter some text before submitting.")
            return redirect('webpage1')

        try:
            UserWork.objects.create(
                user=request.user,
                username=request.user.username,
                freewriting=freewriting,
                title=title or 'Untitled Work',
                author=author or request.user.username,
            )
            messages.success(request, "Your work has been submitted successfully!")
            return redirect('webpage1')
        except Exception:
            messages.error(request, "An error occurred while submitting your work. Please try again.")
            return redirect('webpage1')

    user_works = UserWork.objects.all().order_by('-submitted_date')
    context = {
        'user_works': user_works,
        'request_user': request.user,
    }
    return render(request, 'webpage1.html', context)


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


@login_required(login_url='login_user')
@require_http_methods(["GET", "POST"])
def edit_work(request, work_id):
    """Allow the owner to edit only their own work."""
    work = get_object_or_404(UserWork, id=work_id)
    if work.user != request.user:
        messages.error(request, "You can only edit your own work.")
        return redirect('view_user_work', work_id=work.id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        freewriting = request.POST.get('freewriting', '').strip()

        if not freewriting:
            messages.error(request, "Work content cannot be empty.")
            return redirect('edit_work', work_id=work.id)

        work.title = title or 'Untitled Work'
        work.author = author or request.user.username
        work.freewriting = freewriting
        work.save(update_fields=['title', 'author', 'freewriting'])
        messages.success(request, "Your work has been updated successfully.")
        return redirect('view_user_work', work_id=work.id)

    context = {'user_work': work}
    return render(request, 'edit_work.html', context)


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def delete_work(request, work_id):
    """Allow the owner to delete only their own work."""
    work = get_object_or_404(UserWork, id=work_id)
    if work.user != request.user:
        messages.error(request, "You can only delete your own work.")
        return redirect('view_user_work', work_id=work.id)

    work.delete()
    messages.success(request, "Your work has been deleted.")
    return redirect('webpage1')


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def toggle_like(request, work_id):
    """Toggle likes on community work."""
    work = get_object_or_404(UserWork, id=work_id)
    like, created = WorkLike.objects.get_or_create(work=work, user=request.user)
    if not created:
        like.delete()
    return redirect('view_user_work', work_id=work.id)


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def add_comment(request, work_id):
    """Add a comment to community work."""
    work = get_object_or_404(UserWork, id=work_id)
    text = request.POST.get('text', '').strip()

    if not text:
        messages.error(request, "Comment cannot be empty.")
        return redirect('view_user_work', work_id=work.id)

    WorkComment.objects.create(work=work, user=request.user, text=text)
    return redirect('view_user_work', work_id=work.id)


@login_required(login_url='login_user')
@require_http_methods(["GET"])
def view_user_work(request, work_id):
    """Display full view of a single user work and community interactions."""
    try:
        user_work = UserWork.objects.get(id=work_id)
    except UserWork.DoesNotExist:
        messages.error(request, "The work you're looking for doesn't exist.")
        return redirect('webpage1')

    comments = user_work.comments.select_related('user').all()
    user_has_liked = user_work.likes.filter(user=request.user).exists()
    context = {
        'user_work': user_work,
        'comments': comments,
        'total_likes': user_work.total_likes,
        'total_comments': user_work.total_comments,
        'user_has_liked': user_has_liked,
        'is_owner': user_work.user == request.user,
    }
    return render(request, 'webpageuserwork.html', context)