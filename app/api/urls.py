from django.urls import path

#Imports all views from view.py
from . import views

urlpatterns = [
   #Missionary List, Create URL
   path('Missionary/', views.Missionary_LC_view.as_view(), name = "Missionary-list-create"),
   #Missionary Retrieve, Update, Delete URL
   path('Missionary/<int:pk>/', views.Missionary_RUD_view.as_view(), name = "Missionary-retrieve-update-delete"),

   #Church List, Create URL
   path('Church/', views.Church_LC_view.as_view(), name = "Church-list-create"),
   #Church Retrieve, Update, Delete URL
   path('Church/<int:pk>/', views.Church_RUD_view.as_view(), name = "Church-retrieve-update-delete")
]

