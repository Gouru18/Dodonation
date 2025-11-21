"""from django.db import models
from users.models import Donor, Receiver   # import from your users app

class DonationPost(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Clothes', 'Clothes'),
        ('Furniture', 'Furniture'),
        ('Other', 'Other'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_posts')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='Available')
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # For NGO requests
    requested_by = models.ForeignKey(Receiver, null=True, blank=True, related_name='requested_donations', on_delete=models.SET_NULL)
    is_requested = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.donor.username})"


class ProblemReport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"""

from users.forms import DonationForm