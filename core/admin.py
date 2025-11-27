from django.contrib import admin
from django.utils.html import format_html
from .models import Donation, ClaimRequest, GeneralReview, Report
from users.models import User

# --- Custom Admin Site Settings ---
admin.site.site_header = "DoDonation Administration"
admin.site.site_title = "DoDonation Admin"
admin.site.index_title = "Welcome to DoDonation Admin Panel"

# ---------------------- DONATION ADMIN ----------------------


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor_username', 'category', 'status', 'expiry_date', 'date_created')
    list_filter = ('category', 'status')
    # search by donor's username (through donor -> user)
    search_fields = ('title', 'description', 'donor__user__username')
    readonly_fields = ('date_created',)

    def donor_username(self, obj):
        return obj.donor.user.username if obj.donor and obj.donor.user else '(unknown)'
    donor_username.short_description = 'Donor'


# ---------------------- CLAIM REQUEST ADMIN ----------------------

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('donation', 'receiver', 'status', 'date_requested')
    list_filter = ('status',)
    search_fields = ('donation__title', 'receiver__name')
    readonly_fields = ('date_requested',)
    actions = ['accept_requests', 'reject_requests', 'delete_requests']

    def accept_requests(self, request, queryset):
        count = 0
        for req in queryset.select_related('donation'):
            req.status = 'accepted'
            # mark donation as claimed
            req.donation.status = 'claimed'
            req.donation.save()
            req.save()
            count += 1
        self.message_user(request, f'✓ Accepted {count} request(s).')
    accept_requests.short_description = 'Accept selected claim requests'

    def reject_requests(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'✗ Rejected {updated} request(s).')
    reject_requests.short_description = 'Reject selected claim requests'

    def delete_requests(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'✗ Deleted {count} request(s).')
    delete_requests.short_description = 'Delete selected claim requests'


# ---------------------- GENERAL REVIEW ADMIN ----------------------
@admin.register(GeneralReview)
class GeneralReviewAdmin(admin.ModelAdmin):
    list_display = ('review_author', 'email', 'message_preview', 'created_at')
    readonly_fields = ('created_at',)
    actions = ['delete_inappropriate_reviews']

    def review_author(self, obj):
        if obj.user:
            return f"{obj.user.username} (User)"
        return f"{obj.name} (Anonymous)"

    def message_preview(self, obj):
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message

    def delete_inappropriate_reviews(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Deleted {count} review(s).')


# ---------------------- REPORT ADMIN ----------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_author', 'email', 'message', 'created_at')
    readonly_fields = ('created_at',)

    def report_author(self, obj):
        if obj.user:
            return f"{obj.user.username} (User ID: {obj.user.id})"
        return obj.name

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
 
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