from django.contrib import admin
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
    