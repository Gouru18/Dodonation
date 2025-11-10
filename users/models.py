from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)

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
