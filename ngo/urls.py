from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ngo_signup_view, name='ngo_signup'),
    path('pending/', views.ngo_pending_view, name='ngo_pending'),
    path('account/', views.ngo_account_view, name='ngo_account'),
    path('account/edit/', views.ngo_edit_view, name='ngo_edit'),
    path('public/<int:ngo_Id>/', views.ngo_public_profile, name='ngo_public_profile'),
]