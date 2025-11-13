from django.urls import path
from . import views

urlpatterns = [
    # This will be the URL '/review/'
    path('', views.about, name='about'),
]