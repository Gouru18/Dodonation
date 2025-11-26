from django.contrib import admin
from django.utils.html import format_html
from .models import User

"""
# --- Custom Admin Site Settings ---
admin.site.site_header = "DoDonation Administration"
admin.site.site_title = "DoDonation Admin"
admin.site.index_title = "Welcome to DoDonation Admin Panel
"""


"""
class DoDonationAdminSite(admin.AdminSite):
    site_header = "DoDonation Administration"
    site_title = "DoDonation Admin"
    index_title = "Admin Dashboard"

    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }
"""
"""
# ---------------------- USER ADMIN ----------------------
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_no', 'role', 'is_active', 'account_status_badge')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email')

    fieldsets = (
        ('User Information', {'fields': ('username', 'email', 'phone_no', 'role')}),
        ('Account Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('username', 'last_login', 'date_joined')
    actions = ['suspend_account', 'activate_account']

    def account_status_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span style="color: purple; font-weight: bold;">⭐ Superuser</span>')
        elif obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Suspended</span>')

    account_status_badge.short_description = 'Status'

    def suspend_account(self, request, queryset):
        queryset = queryset.exclude(is_superuser=True)
        updated = queryset.update(is_active=False)
        self.message_user(request, f'✗ Suspended {updated} account(s).')

    def activate_account(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✓ Activated {updated} account(s).')
"""

# Apply custom admin
#admin.site.__class__ = DoDonationAdminSite






   

"""@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor_name', 'category', 'status', 'expiry_date', 'created_date')
    search_fields = ('title', 'description', 'donor__username')
    list_filter = ('category', 'status')

    readonly_fields = ('date_created',)

    def donor_name(self, obj):
        return obj.donor.username

    def created_date(self, obj):
        return obj.date_created.strftime('%Y-%m-%d %H:%M')

    actions = ['delete_inappropriate_posts']

    def delete_inappropriate_posts(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Deleted {count} post(s).')"""

