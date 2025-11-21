from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignupForm, DonorSignupForm, ReceiverSignupForm, LoginForm
from .models import ClaimRequest, Donor, Receiver, User, Donation
from django.db.models import Sum

def donor_signup_view(request):
    if request.method == 'POST':
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "donor"  
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
            user.role = "ngo"        
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
                if user.role == "ngo" and not user.is_active:
                    messages.info(request, "Your NGO verification is still pending.")
                    return redirect('homepage')

                login(request, user)
                # Use messages.success for login success (will be converted to alert in template)
                messages.success(request, f"Welcome back, {user.username}!", extra_tags='alert')
                
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

from .models import Report
from .forms import ReportForm

def leave_report(request):
    # Handle form submission
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_report')  # Redirect back to the same page
    else:
        form = ReportForm()  # Empty form for GET request

    # Fetch all existing reports to display
    reports = Report.objects.order_by('-created_at')  # Newest first

    context = {
        'form': form,
        'reports': reports
    }
    return render(request, 'users/leave_report.html', context)


def homepage(request):

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
    donation_count = Donation.objects.count()
    total_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'users/about.html', {
        'donation_count': donation_count,
        'total_quantity': total_quantity,
    })


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

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Donation

def donation_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    donations = Donation.objects.all()

    if query:
        donations = donations.filter(
            Q(title__icontains=query) | Q(donor__username__icontains=query)
        )
    if category:
        donations = donations.filter(category=category)

    # Handle NGO claiming a donation
    if request.method == 'POST':
        if not request.user.is_authenticated or not hasattr(request.user, 'receiver'):
            messages.error(request, "You must be logged in as an NGO to claim a donation.")
            return redirect('login')

        donation_id = request.POST.get('donation_id')
        donation = get_object_or_404(Donation, id=donation_id)
        receiver = request.user.receiver

        # Avoid duplicate claims
        if not ClaimRequest.objects.filter(donation=donation, receiver=receiver).exists():
            ClaimRequest.objects.create(donation=donation, receiver=receiver, status='pending')
            messages.success(request, "You have successfully requested this donation!")

        return redirect('donation_list')

    context = {
        'donations': donations,
        'query': query,
        'category': category,
    }
    return render(request, 'users/donation_list.html', context)
from django.contrib.auth.decorators import login_required
from .forms import DonorProfileForm, DonationForm
from django.shortcuts import get_object_or_404

@login_required
def donor_profile(request):
    donor = request.user
    donations = donor.donations.all().order_by('-date_created')

    # Handle profile update
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = DonorProfileForm(request.POST, instance=donor)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('donor_profile')
    else:
        profile_form = DonorProfileForm(instance=donor)

    # Handle new donation
    if request.method == 'POST' and 'create_donation' in request.POST:
        donation_form = DonationForm(request.POST, request.FILES)
        if donation_form.is_valid():
            new_donation = donation_form.save(commit=False)
            new_donation.donor = donor
            new_donation.save()
            messages.success(request, "Donation post created!")
            return redirect('donor_profile')
    else:
        donation_form = DonationForm()

    context = {
        'profile_form': profile_form,
        'donation_form': donation_form,
        'donations': donations
    }
    return render(request, 'users/donor_profile.html', context)



@login_required
def edit_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, "Donation updated!")
            return redirect('donor_profile')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'users/edit_donation.html', {'form': form})

@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, "Donation deleted!")
        return redirect('donor_profile')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'users/edit_donation.html', {'form': form})
    # Optional: confirm screen
    #return render(request, 'users/confirm_delete.html', {'donation': donation})

"""@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    donation.delete()
    messages.success(request, "Donation deleted!")
    return redirect('donor_profile')"""

@login_required
def donation_requests(request):
    # Get all claim requests for donations by this donor
    requests = ClaimRequest.objects.filter(donation__donor=request.user)

    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = get_object_or_404(ClaimRequest, id=req_id)
        if action == 'accept':
            req.status = 'accepted'
            req.donation.status = 'claimed'  # from Donation.STATUS
            req.donation.save()
            req.save()
        elif action == 'reject':
            req.status = 'rejected'
            req.save()
        return redirect('donation_requests')

    return render(request, 'users/donation_requests.html', {'requests': requests})

@login_required
def ngo_public_profile(request, ngo_id):
    # Get the NGO object (Receiver)
    ngo = get_object_or_404(Receiver, id=ngo_id)
    
    # Optional: show donations requested by this NGO
    requests_made = ngo.requests.all()  # Assuming ClaimRequest has receiver foreign key
    
    context = {
        'ngo': ngo,
        'requests_made': requests_made,
    }
    return render(request, 'users/ngo_public_profile.html', context)

def donor_public_profile(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    donations = donor.donations.filter(status='available')  # Or show all

    context = {
        'donor': donor,
        'donations': donations,
    }
    return render(request, 'users/donor_public_profile.html', context)
