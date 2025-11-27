from django.contrib import admin
from .models import NGOProfile


@admin.register(NGOProfile)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'name', 'user_email', 'reg_number', 'user_is_active', 'user_date_joined')
    search_fields = ('user__username', 'user__email', 'name', 'reg_number')
    # removed destructive 'delete_ngo' action to prevent accidental deletion of NGO accounts
    actions = ['approve_and_activate_ngo', 'suspend_ngo']

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