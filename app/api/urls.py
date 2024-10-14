from django.urls import path, include

#Imports all views from view.py
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'missionary', views.Missionary_view_set)
router.register(r'church', views.Church_view_set)

urlpatterns = [
   #Router URLs
   path('', include(router.urls)),
   #path ('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
   path('home/', views.home, name = 'home'),

   #Missionary List, Create URL
   path('missionary/',          views.Missionary_LC_view.as_view(),  name = "Missionary-List-Create"),
   #Missionary Retrieve, Update, Delete URL
   path('missionary/<int:pk>/', views.Missionary_RUD_view.as_view(), name = "Missionary-Retrieve-Update-Delete"),

   #Church List, Create URL
   path('church/',          views.Church_LC_view.as_view(),  name = "Church-List-Create"),
   #Church Retrieve, Update, Delete URL
   path('church/<int:pk>/', views.Church_RUD_view.as_view(), name = "Church-Retrieve-Update-Delete")
]

