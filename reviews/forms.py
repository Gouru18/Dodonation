from django import forms
from .models import GeneralReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = GeneralReview
        fields = ['name', 'email', 'message']