"""from django.contrib import admin
from users.models import Donation, Problem, ClaimRequest

@admin.register(Donation)
class DonationPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "donor",
        "category",
        "status",
        "expiry_date",
        "created_at",
        "is_requested",
        "is_accepted"
    )
    list_filter = ("category", "status", "is_requested", "is_accepted", "created_at")
    search_fields = ("title", "description", "donor__username")

    # FIX: donor must be shown so it is NEVER NULL
    fields = (
        "donor",
        "title",
        "description",
        "category",
        "expiry_date",
        "quantity",
        "status",
        "location",
        "image",
        "requested_by",
        "is_requested",
        "is_accepted",
    )

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'category', 'status', 'expiry_date', 'date_created')
    list_filter = ('category', 'status')
    search_fields = ('title', 'description', 'donor__username')
    readonly_fields = ('date_created',)

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('donation', 'receiver', 'status', 'date_requested')
    list_filter = ('status',)
    search_fields = ('donation__title', 'receiver__name')
    readonly_fields = ('date_requested',)

@admin.register(Problem)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at",)
    """
from django.contrib import admin
from .models import DonorProfile

"""
# ---------------------- DONOR ADMIN ----------------------
@admin.register(DonorProfile)
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
"""

@admin.register(DonorProfile)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'user_phone', 'user_is_active', 'user_date_joined', 'organization_name', 'verified')
    search_fields = ('user__username', 'user__email', 'organization_name')
    list_filter = ('verified',)

    def user_username(self, obj):
        return obj.user.username
    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'Username'

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'Email'

    def user_phone(self, obj):
        return obj.user.phone_no
    user_phone.short_description = 'Phone'

    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.boolean = True
    user_is_active.short_description = 'Active'

    def user_date_joined(self, obj):
        return obj.user.date_joined
    user_date_joined.short_description = 'Joined'