from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonationPost
from .forms import DonationPostForm, ProblemReportForm, DonorEditForm
from users.models import Donor, Receiver

@login_required
def donor_account_view(request):
    try:
        donor = Donor.objects.get(username=request.user.username)
    except Donor.DoesNotExist:
        messages.error(request, "You are not authorized as a donor.")
        return redirect('home')

    # Posts belonging to this donor
    own_posts = DonationPost.objects.filter(donor__username=request.user.username).order_by('-created_at')

    # Account page should only show the donor's own posts and profile.
    return render(request, 'donor/account.html', {'own_posts': own_posts})


@login_required
def edit_profile_view(request):
    try:
        donor = Donor.objects.get(username=request.user.username)
    except Donor.DoesNotExist:
        messages.error(request, "You are not authorized as a donor.")
        return redirect('home')

    if request.method == 'POST':
        form = DonorEditForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('donor_account')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DonorEditForm(instance=donor)

    return render(request, 'donor/edit_profile.html', {'form': form})


@login_required
def create_post_view(request):
    try:
        donor = Donor.objects.get(username=request.user.username)
    except Donor.DoesNotExist:
        messages.error(request, "Only donors can create posts.")
        return redirect('home')

    if request.method == 'POST':
        form = DonationPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.donor = donor
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('donor_account')
    else:
        form = DonationPostForm()
    return render(request, 'donor/create_post.html', {'form': form})


@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor__username=request.user.username)
    if request.method == 'POST':
        form = DonationPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('donor_account')
    else:
        form = DonationPostForm(instance=post)
    return render(request, 'donor/edit_post.html', {'form': form})


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor__username=request.user.username)
    post.delete()
    messages.info(request, "Post deleted successfully.")
    return redirect('donor_account')


@login_required
def accept_request_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor__username=request.user.username)
    post.is_accepted = True
    post.status = "Accepted"
    post.save()
    messages.success(request, "Request accepted successfully.")
    return redirect('donor_account')


@login_required
def reject_request_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor__username=request.user.username)
    post.is_requested = False
    post.requested_by = None
    post.status = "Available"
    post.save()
    messages.info(request, "Request rejected successfully.")
    return redirect('donor_account')


def report_problem_view(request):
    if request.method == 'POST':
        form = ProblemReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your problem has been reported successfully.")
            return redirect('home')
    else:
        form = ProblemReportForm()
    return render(request, 'donor/report_problem.html', {'form': form})


@login_required
def donation_requests_view(request):
    """List incoming requests for this donor's posts so they can accept/reject."""
    try:
        donor = Donor.objects.get(username=request.user.username)
    except Donor.DoesNotExist:
        messages.error(request, "You are not authorized as a donor.")
        return redirect('home')

    requests = DonationPost.objects.filter(donor=donor, is_requested=True).order_by('-created_at')
    return render(request, 'donor/requests.html', {'requests': requests})