from django.db import models
from django.db import models
from django.contrib.auth.models import User

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

class Donation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='donation_images/', blank=True, null=True)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')

    def __str__(self):
        return self.title

# Optional: extend user profile for contact info if needed
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

