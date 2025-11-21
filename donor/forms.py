from django import forms
#from .models import DonationPost, ProblemReport
from users.models import Donor, Donation, Report

class DonorEditForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['username', 'email', 'phone_no']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DonationPostForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['donor', 'requested_by', 'created_at']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProblemReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'email', 'message']
