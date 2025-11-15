from django.urls import path
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
   
]
