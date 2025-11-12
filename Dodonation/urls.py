from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported
from core import views as core_views # <-- Add this import

urlpatterns = [
    path('admin/', admin.site.urls),

    # This line makes your 'homepage' view the default page for the site
    path('', core_views.homepage, name='homepage'), # <-- Add this line

    # We can add placeholders for your team's apps
    # path('accounts/', include('accounts.urls')), 
    # path('donations/', include('donations.urls')),
    # path('review/', include('reviews.urls')), 
]