from django.contrib import admin
from django.utils.html import format_html
from .models import User, Donor, Receiver, GeneralReview, Report, Donation, ClaimRequest

# --- Custom Admin Site Settings ---
admin.site.site_header = "DoDonation Administration"
admin.site.site_title = "DoDonation Admin"
admin.site.index_title = "Welcome to DoDonation Admin Panel"

class DoDonationAdminSite(admin.AdminSite):
    site_header = "DoDonation Administration"
    site_title = "DoDonation Admin"
    index_title = "Admin Dashboard"

    class Media:
        css = {
            'all': ('custom_admin.css','users/dodonation_admin.css',)
        }


# Apply custom admin
admin.site.__class__ = DoDonationAdminSite


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
            return format_html('<span style="color: purple; font-weight: bold;"> Superuser</span>')
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


# ---------------------- DONOR ADMIN ----------------------
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_no', 'is_active', 'date_joined')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'email')
    readonly_fields = ('donorID', 'date_joined')

    actions = ['suspend_donors', 'activate_donors']

    def suspend_donors(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'✗ Suspended {updated} donor(s).')

    def activate_donors(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✓ Activated {updated} donor(s).')


# ---------------------- RECEIVER ADMIN (NGO) ----------------------
@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
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


# ---------------------- DONATION ADMIN ----------------------
@admin.register(Donation)
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
        self.message_user(request, f'Deleted {count} post(s).')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "donor":
            kwargs["queryset"] = User.objects.filter(role="donor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ---------------------- CLAIM REQUEST ADMIN ----------------------
@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('donation_title', 'receiver_name', 'status', 'date_requested')
    readonly_fields = ('date_requested',)

    def donation_title(self, obj):
        return obj.donation.title

    def receiver_name(self, obj):
        return obj.receiver.name

    model = Donation
    verbose_name = "Donation request"
    verbose_name_plural = "Donation requests"

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