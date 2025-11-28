import re
from django import forms
from users.models import User
from ngo.models import NGOProfile
from users.forms import UserSignupForm

class NGOSignupForm(UserSignupForm):
    name = forms.CharField(max_length=100, label="NGO Name")
    reg_number = forms.CharField(max_length=50, label="Registration Number")

    class Meta(UserSignupForm.Meta):
        model = User   # still User, not NGOProfile
        # include account fields plus NGO profile fields
        fields = UserSignupForm.Meta.fields + ['name', 'reg_number']  # username, email, phone_no, password, name, reg_number

    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')
        if not re.fullmatch(r'\d{8}', phone):  # exactly 8 digits
            raise forms.ValidationError("Enter a valid 8-digit phone number.")
        return phone

class NGOProfileForm(forms.ModelForm):
    class Meta:
        model = NGOProfile
        fields = ['name', 'reg_number']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no']
        
