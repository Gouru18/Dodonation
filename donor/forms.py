import re
from django import forms
from users.models import User
from core.models import  Report, Donation
from donor.models import DonorProfile

# For editing User fields
class DonorUserEditForm(forms.ModelForm):
    # Allow editing username, email, phone and (optionally) password
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='New password')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
    
    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')
        if not re.fullmatch(r'\d{8}', phone):  # exactly 8 digits
            raise forms.ValidationError("Enter a valid 8-digit phone number.")
        return phone

# For editing donor-specific fields
class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = []


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


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = []


class DonorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password']

    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')
        if not re.fullmatch(r'\d{8}', phone):  # exactly 8 digits
            raise forms.ValidationError("Enter a valid 8-digit phone number.")
        return phone