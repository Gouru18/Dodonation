from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import UserSignupForm, DonorSignupForm, ReceiverSignupForm, LoginForm
from .models import Donor, Receiver
from donor.models import DonationPost


def home_view(request):
    # Show feed of all posts for logged-in users
    posts = DonationPost.objects.all().order_by('-created_at')
    return render(request, 'users/home.html', {'posts': posts})


def donor_signup_view(request):
    if request.method == 'POST':
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DonorSignupForm()

    return render(request, 'users/donor_signup.html', {'form': form})


def ngo_signup_view(request):
    if request.method == 'POST':
        form = ReceiverSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Wait for admin approval
            user.save()
            messages.info(request, "NGO verification is pending. You’ll get access once approved.")
            return redirect('ngo_pending')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReceiverSignupForm()

    return render(request, 'users/ngo_signup.html', {'form': form})


def ngo_pending_view(request):
    return render(request, 'users/ngo_pending.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                # Prevent unapproved NGOs from logging in
                if Receiver.objects.filter(id=user.id).exists() and not user.is_active:
                    messages.info(request, "Your NGO verification is still pending.")
                    return redirect('home')

                login(request, user)
                # Show a one-time welcome message after login (will be displayed by base.html)
                messages.success(request, f"Welcome back, {user.username}!")
                # Redirect to next_page if provided, otherwise use LOGIN_REDIRECT_URL
                next_page = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def select_role_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'donor':
            return redirect('donor_signup')
        elif role == 'ngo':
            return redirect('ngo_signup')
        else:
            messages.error(request, "Please select a role.")
    return render(request, 'users/select_role.html')
