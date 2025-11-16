from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
      path('',views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),  # login page
    path('select-role/', views.select_role_view, name='select_role'),
    path('donor-signup/', views.donor_signup_view, name='donor_signup'),  # donor signup
    path('ngo-signup/', views.ngo_signup_view, name='ngo_signup'),  # NGO signup
    path('ngo-pending/', views.ngo_pending_view, name='ngo_pending'),  # pending page for NGOs
    path('leave_review/', views.leave_review, name='leave_review'),
    path('about/',views.about, name='about'),
    path('ngo_account/', views.ngo_account_view, name='ngo_account'), #NGO_account_view page
    path('logout/', views.logout_view, name='logout'),
    path('leave-report/', views.leave_report, name='leave_report'),
    path('donation_list/',views.donation_list,name='donation_list'),
path('donation_requests/', views.donation_requests, name='donation_requests'),
           path('donor_profile/',views.donor_profile,name='donor_profile'),
path('ngo/<int:ngo_id>/', views.ngo_public_profile, name='ngo_public_profile'),
path('donor_public_profile/<int:donor_id>/', views.donor_public_profile, name='donor_public_profile'),
    path('donation/edit/<int:donation_id>/', views.edit_donation, name='edit_donation'),
    path('donation/delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
]
