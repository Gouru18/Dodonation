from django.contrib import admin
from django import forms
from users.models import User
from .models import NGOProfile


class NGOProfileCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(max_length=8, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='Password (again)')

    class Meta:
        model = NGOProfile
        fields = ['name', 'reg_number']
        labels = {
            'name': 'NGO name',
            'reg_number': 'Registration number',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('The two password fields didn\'t match.')
        return cleaned

    def save(self, commit=True):
        profile = super().save(commit=False)
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        phone_no = self.cleaned_data['phone_no']
        password = self.cleaned_data['password1']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.phone_no = phone_no
        user.role = 'ngo'
        user.save()

        profile.user = user
        if commit:
            profile.save()
        return profile


@admin.register(NGOProfile)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'name', 'user_email', 'reg_number', 'user_is_active', 'user_date_joined')
    search_fields = ('user__username', 'user__email', 'name', 'reg_number')
    # removed destructive 'delete_ngo' action to prevent accidental deletion of NGO accounts
    actions = ['approve_and_activate_ngo', 'suspend_ngo']

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return NGOProfileCreationForm
        return super().get_form(request, obj, **kwargs)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.boolean = True
    user_is_active.short_description = 'Active'

    def user_date_joined(self, obj):
        return obj.user.date_joined
    user_date_joined.short_description = 'Joined'

    # --- Admin actions ---
    def approve_and_activate_ngo(self, request, queryset):
        """Validate, confirm and activate the related user account for selected NGOs."""
        count = 0
        for profile in queryset.select_related('user'):
            # no `is_validated` field any more; just activate the user account
            profile.user.is_active = True
            # give NGO users staff access if you want them to access admin; adjust as needed
            # profile.user.is_staff = True
            profile.user.save()
            count += 1
        self.message_user(request, f'✓ Approved & activated {count} NGO(s).')
    approve_and_activate_ngo.short_description = 'Approve and activate selected NGOs'

    def suspend_ngo(self, request, queryset):
        """Deactivate the related user accounts for selected NGOs."""
        count = 0
        for profile in queryset.select_related('user'):
            profile.user.is_active = False
            profile.user.save()
            count += 1
        self.message_user(request, f'✗ Suspended {count} NGO(s).')
    suspend_ngo.short_description = 'Suspend selected NGOs (deactivate user)'

    # note: delete_ngo action intentionally removed to avoid accidental user deletions