from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from core.models import Donation, ClaimRequest, GeneralReview, Report
from core.forms import ReviewForm, ReportForm, DonationForm
from django.db.models import Sum
from users.decorators import login_required_home
from ngo.views import NGOProfile

def donation_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    donations = Donation.objects.all()

    if query:
        donations = donations.filter(Q(title__icontains=query) | Q(donor__user__username__icontains=query))
    if category:
        donations = donations.filter(category=category)
    if status:
        donations = donations.filter(status=status)

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
        'status': status,
    })

@login_required_home
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

login_required_home
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

def ngo_list(request):
    ngos = NGOProfile.objects.order_by('name')
    return render(request, 'core/ngo_list.html', {'ngos': ngos})

def about(request):
    donation_count = Donation.objects.count()
    # Sum quantities of claimed donations
    total_quantity = Donation.objects.filter(status='claimed').aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'about.html', {
        'donation_count': donation_count,
        'total_quantity': total_quantity,
    })
                                                       



