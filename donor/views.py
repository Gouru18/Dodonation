from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonationPost
from .forms import DonorEditForm, DonationPostForm, ProblemReportForm
from users.models import Donor

@login_required
def donor_account_view(request):
    donor = Donor.objects.get(id=request.user.id)
    posts = DonationPost.objects.filter(donor=donor)

    if request.method == 'POST':
        form = DonorEditForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('donor_account')
    else:
        form = DonorEditForm(instance=donor)

    return render(request, 'donor/account.html', {'form': form, 'posts': posts})


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = DonationPostForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(request, "Donation post created successfully!")
            return redirect('donor_account')
    else:
        form = DonationPostForm()
    return render(request, 'donor/create_post.html', {'form': form})


@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor=request.user)
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
    post = get_object_or_404(DonationPost, id=post_id, donor=request.user)
    post.delete()
    messages.info(request, "Post deleted.")
    return redirect('donor_account')


@login_required
def accept_request_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor=request.user)
    post.status = 'Accepted'
    post.save()
    messages.success(request, "Request accepted!")
    return redirect('donor_account')


@login_required
def reject_request_view(request, post_id):
    post = get_object_or_404(DonationPost, id=post_id, donor=request.user)
    post.requested_by = None
    post.status = 'Available'
    post.save()
    messages.info(request, "Request rejected.")
    return redirect('donor_account')


def report_problem_view(request):
    if request.method == 'POST':
        form = ProblemReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Problem reported successfully!")
            return redirect('report_problem')
    else:
        form = ProblemReportForm()
    return render(request, 'donor/report_problem.html', {'form': form})