from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='donor')

    USERNAME_FIELD = 'username'  # login by username
    REQUIRED_FIELDS = ['email', 'phone_no']

    def __str__(self):
        return self.username


class Donor(User):
    donorID = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Donor: {self.username}"


class Receiver(User):
    receiverID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Receiver: {self.name}"

class GeneralReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Review by {self.user.username}'
        return f'Review by {self.name}'
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Report by {self.user.username}'
        return f'Report by {self.name}'


CATEGORIES = [
    ('food', 'Food'),
    ('clothes', 'Clothes'),
    ('others', 'Others'),
]

STATUS = [
    ('available', 'Available'),
    ('claimed', 'Claimed'),
    ('collected', 'Collected'),
    ('expired', 'Expired'),
]

from django.utils import timezone

class Donation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')

    def save(self, *args, **kwargs):
        # Auto-update status if expiry_date passed
        if self.status == 'available' and self.expiry_date < timezone.now().date():
            self.status = 'expired'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class ClaimRequest(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='claim_requests')
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver.name} -> {self.donation.title} ({self.status})"

    class Meta:
        unique_together = ('donation', 'receiver')  # Prevent the same NGO requesting the same donation multiple times