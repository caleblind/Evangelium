from django.urls import path

#Imports all views from view.py
from . import views

urlpatterns = [
   #Missionary URL
   path('missionary/', views.Missionary_LC_view.as_view(), name = "missionary-list-create"),

   #Church URL
   path('church/', views.Church_LC_view.as_view(), name =  "Church-list-create"),
]

