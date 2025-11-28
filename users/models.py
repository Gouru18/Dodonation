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
    phone_no = models.CharField(max_length=8)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='donor')

    USERNAME_FIELD = 'username'  # login by username
    REQUIRED_FIELDS = ['email', 'phone_no']

    def __str__(self):
        return self.username

