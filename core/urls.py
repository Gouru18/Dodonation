from django.urls import path
from django.shortcuts import render 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', lambda r: render(r,'core/home.html'), name='home'),
    path('donor/account/', views.donor_account, name='donor_account'),
    path('donation/create/', views.create_donation, name='create_donation'),
    path('donation/<int:pk>/edit/', views.edit_donation, name='edit_donation'),
    path('donation/<int:pk>/delete/', views.delete_donation, name='delete_donation'),
    path('ngo/<int:ngo_id>/profile/', views.view_ngo_profile, name='view_ngo_profile'),
    path('request/<int:req_id>/accept/', views.accept_request, name='accept_request'),
    path('request/<int:req_id>/reject/', views.reject_request, name='reject_request'),
    path('report/', views.report_problem, name='report_problem'),
]