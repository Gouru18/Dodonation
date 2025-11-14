from django.urls import path
from . import views

urlpatterns = [
    # This will be the URL 'about'
    path('about/', views.about, name='about'),
]