from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from users.models import User
import re

# Common User Signup Form
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

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password"
    )
