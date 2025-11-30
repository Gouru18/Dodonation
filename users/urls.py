from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('select-role/', views.select_role_view, name='select_role'),
    path('', views.homepage, name='homepage'),
]