from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Donation, ClaimRequest
from core.forms import DonationForm
from donor.models import DonorProfile
from donor.forms import DonorProfileForm, DonorSignupForm, DonorUserEditForm
from django.contrib.auth import update_session_auth_hash


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
    # Try to get donor profile, create if it doesn't exist
    donor_profile = getattr(user, "donor_profile", None)
    if donor_profile is None:
        donor_profile = DonorProfile(user=user)
        donor_profile.save()

    if request.method == "POST":
        # Updating profile
        if "update_profile" in request.POST:
            user_form = DonorUserEditForm(request.POST, instance=user)
            profile_form = DonorProfileForm(request.POST, request.FILES, instance=donor_profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()

                profile = profile_form.save(commit=False)
                profile.user = user  # make sure user is attached
                profile.save()

                # Keep user logged in even if username/email changes
                update_session_auth_hash(request, user)

                messages.success(request, "Profile updated successfully!")
                return redirect("donor_profile")

        # Creating new donation
        elif "create_donation" in request.POST:
            donation_form = DonationForm(request.POST, request.FILES)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.donor = donor_profile
                donation.save()
                messages.success(request, "Donation posted successfully!")
                return redirect("donor_profile")
    else:
        user_form = DonorUserEditForm(instance=user)
        profile_form = DonorProfileForm(instance=donor_profile)
        donation_form = DonationForm()

    donations = Donation.objects.filter(donor=donor_profile).order_by("-date_created")

    return render(
        request,
        "donor/donor_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "donation_form": donation_form,
            "donations": donations,
        },
    )


@login_required
def edit_donation(request, donation_id):
    donor_profile = getattr(request.user, 'donor_profile', None)
    donation = get_object_or_404(Donation, id=donation_id, donor=donor_profile)
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
    donor_profile = getattr(request.user, 'donor_profile', None)
    donation = get_object_or_404(Donation, id=donation_id, donor=donor_profile)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, "Donation deleted!")
        return redirect('donor_profile')
    return redirect('donor_profile')  # fallback


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
            req.donation.status = 'claimed'
            req.donation.save()
            req.save()
        elif action == 'reject':
            req.status = 'rejected'
            req.save()
        return redirect('donation_requests')

    return render(request, 'donor/donation_requests.html', {'requests': requests})


def donor_public_profile(request, donor_id):
    donor_profile = get_object_or_404(DonorProfile, pk=donor_id)
    donations = donor_profile.donations.all()
    return render(request, 'donor/donor_public_profile.html', {'donor': donor_profile.user, 'donations': donations})
