from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from donations.models import Donation
from django.contrib.auth.models import User
from django.db.models import Q

def donation_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    donations = Donation.objects.all() # pylint: disable=no-member

    if query:
        donations = donations.filter(
            Q(title__icontains=query) | Q(donor__username__icontains=query)
        )
    if category:
        donations = donations.filter(category=category)

    return render(request, 'donations/donation_list.html', {
        'donations': donations,
        'category': category,
        'query': query,
    })


def donor_profile(request, donor_id):
    donor = get_object_or_404(User, pk=donor_id)
    donations = donor.donations.all()
    # Assume UserProfile is linked to User model using OneToOneField
    profile = getattr(donor, 'userprofile', None)
    return render(request, 'donations/donor_profile.html', {
        'donor': donor,
        'profile': profile,
        'donations': donations,
    })

