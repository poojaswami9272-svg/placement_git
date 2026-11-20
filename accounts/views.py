from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import StudentRegistrationForm, CustomLoginForm
from notifications.models import Notification

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Create welcome notification
            Notification.objects.create(
                user=user,
                title="Welcome to AI Placement Portal!",
                message=f"Hello {user.first_name or user.username}! Your student profile has been created. Complete your resume to start applying.",
                notification_type='SYSTEM',
                link_url='/students/profile/'
            )
            messages.success(request, f"Welcome to AI Placement Portal, {user.first_name or user.username}! Your registration was successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('home')
