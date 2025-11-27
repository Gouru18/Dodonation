from django.contrib import admin
from .models import NGOProfile


"""
# ---------------------- RECEIVER ADMIN (NGO) ----------------------
@admin.register(NGOProfile)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'reg_number', 'is_validated', 'is_confirmed', 'is_active', 'date_joined')
    list_filter = ('is_validated', 'is_confirmed', 'is_active')
    search_fields = ('username', 'email', 'name', 'reg_number')

    fieldsets = (
        ('NGO Information', {'fields': ('username', 'email', 'name', 'reg_number', 'phone_no')}),
        ('Validation', {'fields': ('is_validated', 'is_confirmed')}),
        ('Account Status', {'fields': ('is_active',)}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

    readonly_fields = ('receiverID', 'date_joined', 'last_login', 'username')
    actions = ['validate_ngo_existence', 'confirm_ngo_registration', 'approve_and_activate_ngo', 'reject_ngo', 'suspend_ngo']

    def validate_ngo_existence(self, request, queryset):
        updated = queryset.update(is_validated=True)
        self.message_user(request, f'✓ Validated {updated} NGO(s).')

    def confirm_ngo_registration(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f'✓ Confirmed {updated} NGO(s).')

    def approve_and_activate_ngo(self, request, queryset):
        updated = queryset.update(is_validated=True, is_confirmed=True, is_active=True)
        self.message_user(request, f'✓ Approved & activated {updated} NGO(s).')

    def reject_ngo(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'✗ Deleted {count} NGO(s).')

    def suspend_ngo(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'✗ Suspended {updated} NGO(s).')
"""


@admin.register(NGOProfile)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'name', 'user_email', 'reg_number', 'is_validated', 'is_confirmed', 'user_is_active', 'user_date_joined')
    search_fields = ('user__username', 'user__email', 'name', 'reg_number')
    list_filter = ('is_validated', 'is_confirmed')

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