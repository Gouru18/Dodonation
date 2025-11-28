from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.donor_signup_view, name='donor_signup'),
    path('profile/', views.donor_profile, name='donor_profile'),
    path('donation/edit/<int:donation_id>/', views.edit_donation, name='edit_donation'),
    path('donation/delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('requests/', views.donation_requests, name='donation_requests'),
    path('public/<int:donor_id>/', views.donor_public_profile, name='donor_public_profile'),
]