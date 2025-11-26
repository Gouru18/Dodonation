from django.db import models
from users.models import User

class NGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ngo_profile")
    receiverID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=50)
    is_validated = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"NGO: {self.name}"
