from django.contrib import admin
from .models import DonationPost, ProblemReport

@admin.register(DonationPost)
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


@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at",)