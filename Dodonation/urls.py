from django.contrib import admin
from django.urls import path, include  
from core import views as core_views   

urlpatterns = [
    path('admin/', admin.site.urls),

    #  from 'yogendra-homepage' branch
    path('', core_views.homepage, name='homepage'),

    # from 'yogendra-review-page' branch
    path('review/', include('reviews.urls')),

    # placeholders other' apps

    # for the 'About' page, testing which is correct url path
    path('about/',core_views.about,name='about'),
    path('',include('core.urls')),

    # path('accounts/', include('accounts.urls')), 
    # path('donations/', include('donations.urls')),
]