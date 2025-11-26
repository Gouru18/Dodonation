
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Donation, ClaimRequest
from core.forms import DonationForm
from donor.models import DonorProfile
from donor.forms import DonorProfileForm, DonorSignupForm, DonorUserEditForm



def donor_signup_view(request):
    if request.method == 'POST':
        user_form = DonorSignupForm(request.POST)
        profile_form = DonorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = "donor"
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            donor_profile = profile_form.save(commit=False)
            donor_profile.user = user
            donor_profile.save()

            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')
    else:
        user_form = DonorSignupForm()
        profile_form = DonorProfileForm()
    return render(request, 'donor/donor_signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def donor_profile(request):
    user = request.user
    donor_profile = getattr(user, "donor_profile", None)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = DonorUserEditForm(request.POST, instance=user)
            profile_form = DonorProfileForm(request.POST, instance=donor_profile)
            donation_form = DonationForm()  # empty form
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('donor_profile')

        elif 'create_donation' in request.POST:
            user_form = DonorUserEditForm(instance=user)
            profile_form = DonorProfileForm(instance=donor_profile)
            donation_form = DonationForm(request.POST, request.FILES)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.donor = donor_profile   # link to donor profile
                donation.save()
                messages.success(request, "Donation posted successfully!")
                return redirect('donor_profile')

    else:
        user_form = DonorUserEditForm(instance=user)
        profile_form = DonorProfileForm(instance=donor_profile)
        donation_form = DonationForm()

    donations = Donation.objects.filter(donor=donor_profile)

    return render(request, 'donor/donor_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'donation_form': donation_form,
        'donations': donations,
    })


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
    return render(request, 'core/edit_donation.html', {'form': form})

@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, "Donation deleted!")
        return redirect('donor_profile')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'core/edit_donation.html', {'form': form})
    # Optional: confirm screen
    #return render(request, 'users/confirm_delete.html', {'donation': donation})


@login_required
def donation_requests(request):
    donor = getattr(request.user, "donor_profile", None)
    # Get all claim requests for donations by this donor
    requests = ClaimRequest.objects.filter(donation__donor=donor).select_related('donation', 'receiver')

    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = get_object_or_404(ClaimRequest, id=req_id, donation__donor=donor)
        if action == 'accept':
            req.status = 'accepted'
            req.donation.status = 'claimed'  # from Donation.STATUS
            req.donation.save()
            req.save()
        elif action == 'reject':
            req.status = 'rejected'
            req.save()
        return redirect('donation_requests')

    return render(request, 'donor/donation_requests.html', {'requests': requests})

"""
def donor_public_profile(request, donor_id):
    donor = get_object_or_404(DonorProfile, id=donor_id)
    donations = donor.donations.filter(status='available')  # Or show all

    context = {
        'donor': donor,
        'donations': donations,
    }
    return render(request, 'donor/donor_public_profile.html', context)
"""

def donor_public_profile(request, donor_id):
    donor_profile = get_object_or_404(DonorProfile, id=donor_id)
    return render(request, 'donor/public_profile.html', {'donor_profile': donor_profile})
