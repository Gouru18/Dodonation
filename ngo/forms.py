from django import forms
from users.models import User
from ngo.models import NGOProfile
from users.forms import UserSignupForm


class DonorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password']



class NGOSignupForm(UserSignupForm):
    name = forms.CharField(max_length=100, label="NGO Name")
    reg_number = forms.CharField(max_length=50, label="Registration Number")

    class Meta(UserSignupForm.Meta):
        model = User   # still User, not NGOProfile
        fields = UserSignupForm.Meta.fields  # username, email, phone_no, password

"""class NGOProfileForm(forms.ModelForm):
    class Meta:
        model = NGOProfile
        fields = ['name', 'reg_number']"""

"""
# -------------------------
# Receiver (NGO) Signup Form
# -------------------------
class NGOSignupForm(UserSignupForm):
    name = forms.CharField(max_length=100, label="NGO Name")
    reg_number = forms.CharField(max_length=50, label="Registration Number")

    class Meta(UserSignupForm.Meta):
        model = NGOProfile
        fields = UserSignupForm.Meta.fields + ['name', 'reg_number']
"""