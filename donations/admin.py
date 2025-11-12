from django.contrib import admin
from donations.models import Donation, UserProfile

admin.site.register(Donation)
admin.site.register(UserProfile)
