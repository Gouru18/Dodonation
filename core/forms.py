from django import forms
from django.core.exceptions import ValidationError
from core.models import GeneralReview, Donation
import re

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



class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'category', 'quantity', 'expiry_date', 'location', 'image']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}), 
        }
