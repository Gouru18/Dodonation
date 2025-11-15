from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignupForm, DonorSignupForm, ReceiverSignupForm, LoginForm
from .models import Donor, Receiver

def donor_signup_view(request):
    if request.method == 'POST':
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "donor"     # <<< ADD THIS LINE
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
            user.role = "ngo"        # <<< ADD THIS LINE
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
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
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

from .models import GeneralReview
from .forms import ReviewForm

def leave_review(request):
    # This handles when a user submits the form
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_review') # Redirect back to the same page

    # This handles when a user just visits the page (a GET request)
    else:
        form = ReviewForm() # Give them a blank form

    # Get all existing reviews from the database to show them
    reviews = GeneralReview.objects.order_by('-created_at') # Newest first

    context = {
        'form': form,
        'reviews': reviews
    }
    return render(request, 'users/leave_review.html', context)

def homepage(request):
    # This page is for your Task 6.
    # [cite_start]Your System Spec shows the Donation model has a 'date_created' field[cite: 204].

    # --- FOR TESTING ---
    # We can't get real donations yet (Poshita/Vedna's task).
    # So, we will use a "dummy" list to build your template.
    recent_donations = [
        {'title': 'Sample Donation 1', 'description': 'Test desc', 'category': 'Food', 'quantity': 10, 'location': 'Here'},
        {'title': 'Sample Donation 2', 'description': 'Test desc', 'category': 'Clothing', 'quantity': 5, 'location': 'There'},
        {'title': 'Sample Donation 3', 'description': 'Test desc', 'category': 'Other', 'quantity': 2, 'location': 'Anywhere'},
    ]

    context = {
        'recent_donations': recent_donations
    }
    return render(request, 'users/homepage.html', context)

def about(request):
    return render(request, 'users/about.html')


def ngo_account_view(request):
    user = request.user
    if not hasattr(user, 'receiver'):
        return redirect('homepage')  # safety check

    receiver = user.receiver

    # Donations claimed by this NGO
    claimed = ClaimRequest.objects.filter(receiver=receiver, status='Accepted')

    # Requests sent by this NGO
    requests = ClaimRequest.objects.filter(receiver=receiver)

    # Stats
    total_requests = requests.count()
    total_claimed = claimed.count()
    success_rate = round((total_claimed / total_requests) * 100, 2) if total_requests else 0

    context = {
        'receiver': receiver,
        'requests': requests,
        'claimed': claimed,
        'stats': {
            'total_requests': total_requests,
            'total_claimed': total_claimed,
            'success_rate': success_rate,
        }
    }
    return render(request, 'users/ngo_account.html', context)