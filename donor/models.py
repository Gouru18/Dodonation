from django.db import models
from users.models import Donor, Receiver  # import your user types
from django.utils import timezone

class DonationPost(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Available')
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    requested_by = models.ForeignKey(Receiver, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.donor.username}"


class ProblemReport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue by {self.name}"