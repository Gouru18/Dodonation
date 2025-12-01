from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignupForm, LoginForm
from users.models import User
from django.db.models import Sum
from core.models import Donation

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                # Prevent unapproved NGOs from logging in
                if user.role == "ngo" and not user.is_active:
                    messages.info(request, "Your NGO verification is still pending.")
                    return redirect('homepage')

                login(request, user)
                # Use messages.success for login success (will be converted to alert in template)
                # messages.success(request, f"Welcome back, {user.username}!", extra_tags='alert')
                
                # Redirect superusers/staff to admin panel, others to homepage
                if user.is_superuser or user.is_staff:
                    return redirect('admin:index')
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('homepage')



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

def homepage(request):

    recent_donations = (
        Donation.objects
        .filter(status='claimed')            # show only available (not expired/claimed)
        .order_by('-date_created')[:4]         # latest 4
    )

    context = {
        'recent_donations': recent_donations
    }
    return render(request, 'homepage.html', context)






