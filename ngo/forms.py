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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if NGOProfile.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("An NGO with this name already exists.")
        return name

    def clean_reg_number(self):
        reg = self.cleaned_data.get('reg_number')
        if NGOProfile.objects.filter(reg_number__iexact=reg).exists():
            raise forms.ValidationError("An NGO with this registration number already exists.")
        return reg

class NGOProfileForm(forms.ModelForm):
    class Meta:
        model = NGOProfile
        fields = ['name', 'reg_number']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = NGOProfile.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('An NGO with this name already exists.')
        return name

    def clean_reg_number(self):
        reg = self.cleaned_data.get('reg_number')
        qs = NGOProfile.objects.filter(reg_number__iexact=reg)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('An NGO with this registration number already exists.')
        return reg


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no']
        
