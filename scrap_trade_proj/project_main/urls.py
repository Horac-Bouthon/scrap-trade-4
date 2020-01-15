from django.urls import path
from . import views

urlpatterns = [
    path('', views.spa, name='project-home'),
    path('who_are_we/', views.who_are_we, name='who_are_we'),
    path('how_we_work/', views.how_we_work, name='how_we_work'),
    path('partners/', views.partners, name='partners'),
    path('contacts/', views.contacts, name='contacts'),
    path('', views.home_project, name='project-home-old'),
]
