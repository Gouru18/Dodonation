from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
        ('normal', 'Normal'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=30, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
    
class Donation(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('collected', 'Collected'),
        ('expired', 'Expired'),
    ]
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)  # e.g. "3 boxes" or "5 kg"
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='donation_images/', null=True, blank= True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #a flag if an NGO has requested it (determined via DonationRequest)
    def __str__(self):
        return f"{self.title} by {self.donor.username}"
    
class DonationRequest(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='requests')
    ngo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ngo_requests')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(null=True) # None -> pending, True->accepted, False->rejected

    def __str__(self):
        return f"Request by {self.ngo.username} for {self.donation.title}"
    
class ProblemReport(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.name} at {self.created_at}"