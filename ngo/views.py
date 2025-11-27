from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import NGOSignupForm
from core.models import ClaimRequest
from .models import NGOProfile

def ngo_signup_view(request):
    if request.method == 'POST':
        form = NGOSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "ngo"
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # wait for admin approval
            user.save()

            NGOProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                reg_number=form.cleaned_data['reg_number']
            )
            
            messages.info(request, "NGO verification is pending.")
            return redirect('ngo_pending')
    else:
        form = NGOSignupForm()
    return render(request, 'ngo/ngo_signup.html', {'form': form})

def ngo_pending_view(request):
    return render(request, 'ngo/ngo_pending.html')

def ngo_account_view(request):
    ngo_profile = request.user.ngo_profile
    claimed = ClaimRequest.objects.filter(receiver=ngo_profile, status='accepted')
    requests = ClaimRequest.objects.filter(receiver=ngo_profile)

    stats = {
        'total_requests': requests.count(),
        'total_claimed': claimed.count(),
        'success_rate': round((claimed.count() / requests.count()) * 100, 2) if requests else 0,
    }
    return render(request, 'ngo/ngo_account.html', {
        'receiver': ngo_profile,
        'requests': requests,
        'claimed': claimed,
        'stats': stats,
    })

#@login_required
def ngo_public_profile(request, ngo_id):
    # Get the NGO object (Receiver)
    ngo = get_object_or_404(NGOProfile, id=ngo_id)
    
    # Optional: show donations requested by this NGO
    requests_made = ClaimRequest.objects.filter(receiver=ngo).select_related("donation")  # Assuming ClaimRequest has receiver foreign key
    
    context = {
        'ngo': ngo,
        'requests_made': requests_made,
    }
    return render(request, 'ngo/ngo_public_profile.html', context)


