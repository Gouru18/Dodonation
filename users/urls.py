from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # homepage
    path('login/', views.login_view, name='login'),  # login page
    path('select-role/', views.select_role_view, name='select_role'),
    path('donor-signup/', views.donor_signup_view, name='donor_signup'),  # donor signup
    path('ngo-signup/', views.ngo_signup_view, name='ngo_signup'),  # NGO signup
    path('ngo-pending/', views.ngo_pending_view, name='ngo_pending'),  # pending page for NGOs
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
