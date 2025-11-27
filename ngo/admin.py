from django.contrib import admin
from .models import NGOProfile


@admin.register(NGOProfile)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'name', 'user_email', 'reg_number', 'is_validated', 'is_confirmed', 'user_is_active', 'user_date_joined')
    search_fields = ('user__username', 'user__email', 'name', 'reg_number')
    list_filter = ('is_validated', 'is_confirmed')
    actions = ['validate_ngo', 'confirm_ngo', 'approve_and_activate_ngo', 'suspend_ngo', 'delete_ngo']

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
    def validate_ngo(self, request, queryset):
        """Mark selected NGO profiles as validated."""
        updated = queryset.update(is_validated=True)
        self.message_user(request, f'✓ Validated {updated} NGO(s).')
    validate_ngo.short_description = 'Validate selected NGOs'

    def confirm_ngo(self, request, queryset):
        """Mark selected NGO profiles as confirmed/registered."""
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f'✓ Confirmed {updated} NGO(s).')
    confirm_ngo.short_description = 'Confirm selected NGOs'

    def approve_and_activate_ngo(self, request, queryset):
        """Validate, confirm and activate the related user account for selected NGOs."""
        count = 0
        for profile in queryset.select_related('user'):
            profile.is_validated = True
            profile.is_confirmed = True
            profile.save()
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

    def delete_ngo(self, request, queryset):
        """Delete selected NGO profiles and their related user accounts."""
        users = [p.user for p in queryset.select_related('user')]
        count = queryset.count()
        # delete profiles first
        queryset.delete()
        # then delete users (if desired)
        deleted_users = 0
        for u in users:
            try:
                u.delete()
                deleted_users += 1
            except Exception:
                # ignore any user delete errors
                pass
        self.message_user(request, f'✗ Deleted {count} NGO profile(s) and {deleted_users} user account(s).')
    delete_ngo.short_description = 'Delete selected NGOs and their user accounts'