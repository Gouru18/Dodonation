from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Donation, DonationRequest, Profile
from .forms import DonationForm, ProblemReportForm
from django.contrib import messages 
from django.http import JsonResponse, HttpResponseForbidden

def home(request):
    return HttpResponse("Welcome to the Donor Home page!")

@login_required
def donor_account(request):
    if request.user.profile.user_type != 'donor':
        return HttpResponseForbidden("Only donors can access this page.")
    donations = Donation.objects.filter(donor=request.user).order_by("-created_at")
    return render(request, "core/donor_account.html", {'donations': donations})

@login_required
def create_donation(request):
    if request.user.profile.user_type != 'donor':
        return HttpResponseForbidden("Only donors can create donations.")
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            don = form.save(commit=False)
            don.donor = request.user
            don.save()
            messages.success(request, 'Donation posted.')
            return redirect('donor_account')
    else:
        form = DonationForm()
    return render(request,'core/create_donation.html', {'form': form})

@login_required
def edit_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated.')
            return redirect ('donor_account')
        else:
            form = DonationForm(instance=donation)
        return render(request, 'core/edit_donation.html', {'form':form, 'donation':donation})
    
@login_required
def delete_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    if request.method == 'POST':
        donation.delete()
        messages.success(request,'Donation deleted.')
        return redirect('donor_account')
    return render(request,'core/confirm_delete.html', {'donation': donation})

@login_required
def view_ngo_profile(request, ngo_id):
    ngo_user = get_object_or_404(User, id=ngo_id)
    profile = ngo_user.profile
    # This view can return JSON if used by modal via AJAX
    if request.is_ajax():
        return JsonResponse({
            'name': ngo_user.get_full_name() or ngo_user.username,
            'email': ngo_user.email,
            'contact': profile.contact_number,
            'location': profile.location
        })
    return render(request,'core/ngo_profile.html', {'ngo': ngo_user})

@login_required
def accept_request(request, req_id):
    req = get_object_or_404(DonationRequest, id=req_id)
    if req.donation.donor != request.user:
        return HttpResponseForbidden()
    req.accepted = True
    req.save()
    req.donation.status = 'claimed'
    req.donation.save()
    messages.success(request,'Request accepted.')
    return redirect('donor_account')

@login_required
def reject_request(request, req_id):
    req = get_object_or_404(DonationRequest, id=req_id)
    if req.donation.donor != request.user:
        return HttpResponseForbidden()
    req.accepted = False
    req.save()
    messages.info(request,'Request rejected.')
    return redirect('donor_account')


def report_problem(request):
    if request.method == 'POST':
        form = ProblemReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Report submitted. Thank you.')
            return redirect('home')
    else:
        form = ProblemReportForm()
    return render(request,'core/report_problem.html', {'form': form})
