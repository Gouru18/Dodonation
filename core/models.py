from django.db import models
from django.utils import timezone
from users.models import User
from ngo.models import NGOProfile
from donor.models import DonorProfile

CATEGORIES = [
    ('food', 'Food'),
    ('clothes', 'Clothes'),
    ('others', 'Others'),
]

DONATION_STATUS = [
    ('available', 'Available'),
    ('claimed', 'Claimed'),
    ('collected', 'Collected'),
    ('expired', 'Expired'),
]

class Donation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=DONATION_STATUS, default='available')
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='donations')

    def save(self, *args, **kwargs):
        if self.status == 'available' and self.expiry_date < timezone.now().date():
            self.status = 'expired'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.donor.user.username})"

REQUEST_STATUS = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

class ClaimRequest(models.Model):

    donation = models.ForeignKey(
        Donation,
        on_delete=models.CASCADE,
        related_name='claim_requests'
    )
    receiver = models.ForeignKey(
        NGOProfile,
        on_delete=models.CASCADE,
        related_name='claim_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=REQUEST_STATUS,
        default='pending'
    )
    date_requested = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('donation', 'receiver')
        ordering = ['-date_requested']  # newest requests first

    def __str__(self):
        return f"Request by {self.receiver.user.username} for {self.donation.title} ({self.status})"

class GeneralReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username if self.user else self.name}"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username if self.user else self.name}"