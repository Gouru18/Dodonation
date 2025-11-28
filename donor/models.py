from django.db import models
from users.models import User

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="donor_profile")
    donorID = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Donor: {self.user.username}"