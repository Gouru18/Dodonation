from django import forms
#from .models import DonationPost, ProblemReport
from users.models import User
from .models import  DonorProfile
from core.models import  Report, Donation
from donor.models import DonorProfile

# For editing User fields
class DonorUserEditForm(forms.ModelForm):
    # Allow editing username, email, phone and (optionally) password
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='New password')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password']
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

# For editing donor-specific fields
class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ['organization_name']


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


"""
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'category', 'quantity', 'expiry_date', 'location', 'image']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}), 
        }
"""

class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ['organization_name']


class DonorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password']