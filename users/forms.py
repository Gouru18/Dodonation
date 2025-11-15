from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Donor, Receiver
import re

# -------------------------
# Common User Signup Form
# -------------------------
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        min_length=8,
        label="Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password']

    # Validate unique username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Validate email format + uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # regex pattern for valid email (must contain @ and .something)
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValidationError("Please enter a valid email address.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email


# -------------------------
# Donor Signup Form
# -------------------------
class DonorSignupForm(UserSignupForm):
    class Meta(UserSignupForm.Meta):
        model = Donor


# -------------------------
# Receiver (NGO) Signup Form
# -------------------------
class ReceiverSignupForm(UserSignupForm):
    name = forms.CharField(max_length=100, label="NGO Name")
    reg_number = forms.CharField(max_length=50, label="Registration Number")

    class Meta(UserSignupForm.Meta):
        model = Receiver
        fields = UserSignupForm.Meta.fields + ['name', 'reg_number']


# -------------------------
# Login Form
# -------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password"
    )

from .models import GeneralReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = GeneralReview
        fields = ['name', 'email', 'message']

from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'email', 'message']

    # Validate name: not empty and no numbers
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Name cannot be empty.")
        if any(char.isdigit() for char in name):
            raise ValidationError("Name cannot contain numbers.")
        return name

    # Validate email format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValidationError("Please enter a valid email address.")
        return email

    # Validate message: not empty
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise ValidationError("Message cannot be empty.")
        return message

from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'category', 'quantity', 'expiry_date', 'location', 'image_url']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }
class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no']
