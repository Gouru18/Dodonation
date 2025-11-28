from django.contrib import admin
from .models import Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'user_phone', 'user_is_active', 'user_date_joined')
    search_fields = ('user__username', 'user__email')

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