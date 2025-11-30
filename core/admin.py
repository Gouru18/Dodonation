from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Donation, ClaimRequest, GeneralReview, Report
from users.models import User
from ngo.models import NGOProfile
from donor.models import DonorProfile

# --- Custom Admin Site Settings ---
admin.site.site_header = "DoDonation Administration"
admin.site.site_title = "DoDonation Admin"
admin.site.index_title = "Welcome to DoDonation Admin Panel"

# ---------------------- DONATION ADMIN ----------------------

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor_name', 'category', 'status', 'expiry_date', 'created_date')
    search_fields = ('title', 'description', 'donor__user__username')
    list_filter = ('category', 'status')

    readonly_fields = ('date_created',)

    def donor_name(self, obj):
        # `donor` is a DonorProfile; return the related User's username
        return obj.donor.user.username

    def created_date(self, obj):
        return obj.date_created.strftime('%Y-%m-%d %H:%M')

    actions = ['delete_inappropriate_posts']

    def delete_inappropriate_posts(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Deleted {count} post(s).')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "donor":
            # donor FK points to DonorProfile; only allow profiles whose user has role 'donor'
            kwargs["queryset"] = DonorProfile.objects.filter(user__role="donor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    list_display = ('review_author', 'email', 'created_at')
    readonly_fields = ('created_at',)
    actions = ['delete_inappropriate_reviews']

    exclude = ('user',)

    def review_author(self, obj):
        if obj.user:
            return f"{obj.user.username} (User)"
        return f"{obj.name}"

    def delete_inappropriate_reviews(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Deleted {count} review(s).')


# ---------------------- REPORT ADMIN ----------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_author', 'email', 'message', 'created_at')
    readonly_fields = ('created_at',)

    exclude = ('user',)

    def report_author(self, obj):
        if obj.user:
            return f"{obj.user.username} (User ID: {obj.user.id})"
        return obj.name

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
 

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone_no', 'role', 'is_active', 'account_status_badge')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email')

    fieldsets = (
        ('User Information', {'fields': ('username', 'email', 'phone_no', 'role')}),
        ('Account Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsets controls the fields shown on the 'Add user' admin page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_no', 'role', 'password1', 'password2'),
        }),
    )

    actions = ['suspend_account', 'activate_account']

    class Media:
        js = ('users/js/user_admin_inlines.js',)

    # show human-friendly status
    def account_status_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span style="color: purple; font-weight: bold;">✓ Superuser</span>')
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

    # make username editable when adding a user, but keep it readonly when editing
    def get_readonly_fields(self, request, obj=None):
        readonly = ['last_login', 'date_joined']
        if obj:  # editing an existing user
            readonly = ['username', 'last_login', 'date_joined']
        return readonly


# --- Profile inlines so admin can create profile data when creating a user ---
class DonorProfileInline(admin.StackedInline):
    model = DonorProfile
    can_delete = False
    verbose_name_plural = 'Donor profile'
    fk_name = 'user'


class NGOProfileInline(admin.StackedInline):
    model = NGOProfile
    can_delete = False
    verbose_name_plural = 'NGO profile'
    fk_name = 'user'
    fields = ('name', 'reg_number')


# attach both inlines to the User admin; admin can fill NGO fields at user creation
CustomUserAdmin.inlines = (DonorProfileInline, NGOProfileInline)









