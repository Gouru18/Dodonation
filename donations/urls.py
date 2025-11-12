from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
    path('donor/<int:donor_id>/', views.donor_profile, name='donor_profile'),
]
