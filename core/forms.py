from django import forms
from .models import Donation, ProblemReport
from django.contrib.auth.models import User

class DonationForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    class Meta:
        model = Donation
        fields = ['title','description','category','quantity','expiry_date','location','image','status']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }

class ProblemReportForm(forms.ModelForm):
    class Meta:
        model = ProblemReport
        fields = ['name','email','message']
        widgets = {'message': forms.Textarea(attrs={'rows':4})}