from django.urls import path, include

#Imports all views from view.py
from . import views

urlpatterns = [
   path('missionaries/', views.missionaries, name = 'missionaries'),
   path('churches/', views.churches, name = 'churches'),
   path('users/', views.users, name = 'users'),
   path('christian/', views.christian, name = 'christian'),

]

