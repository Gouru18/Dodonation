from django.urls import path
from . import views

urlpatterns = [
    path('donations/', views.donation_list, name='donation_list'),
    path('reviews/', views.leave_review, name='leave_review'),
    path('reports/', views.leave_report, name='leave_report'),
    path('ngo_list/', views.ngo_list, name='ngo_list'),
    path('about/', views.about, name='about'),
]