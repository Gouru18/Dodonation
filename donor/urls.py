from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.donor_account_view, name='donor_account'),
    path('create/', views.create_post_view, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('accept/<int:post_id>/', views.accept_request_view, name='accept_request'),
    path('reject/<int:post_id>/', views.reject_request_view, name='reject_request'),
    path('requests/', views.donation_requests_view, name='donation_requests'),
    path('report/', views.report_problem_view, name='report_problem'),
    path('profile/', views.edit_profile_view, name='edit_profile'),
]
