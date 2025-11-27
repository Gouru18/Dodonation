from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from core.models import Donation, ClaimRequest, GeneralReview, Report
from core.forms import ReviewForm, ReportForm, DonationForm
from django.db.models import Sum

def donation_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    donations = Donation.objects.all()

    if query:
        donations = donations.filter(Q(title__icontains=query) | Q(donor__username__icontains=query))
    if category:
        donations = donations.filter(category=category)

    if request.method == 'POST':
        if not request.user.is_authenticated or not hasattr(request.user, 'ngo_profile'):
            messages.error(request, "You must be logged in as an NGO to claim a donation.")
            return redirect('login')

        donation_id = request.POST.get('donation_id')
        donation = get_object_or_404(Donation, id=donation_id)
        receiver = request.user.ngo_profile

        if not ClaimRequest.objects.filter(donation=donation, receiver=receiver).exists():
            ClaimRequest.objects.create(donation=donation, receiver=receiver, status='pending')
            messages.success(request, "You have successfully requested this donation!")

        return redirect('donation_list')

    return render(request, 'core/donation_list.html', {
        'donations': donations,
        'query': query,
        'category': category,
    })

def leave_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_review')
    else:
        form = ReviewForm()
    reviews = GeneralReview.objects.order_by('-created_at')
    return render(request, 'core/leave_review.html', {'form': form, 'reviews': reviews})

def leave_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_report')
    else:
        form = ReportForm()
    reports = Report.objects.order_by('-created_at')
    return render(request, 'core/leave_report.html', {'form': form, 'reports': reports})
                                                       



