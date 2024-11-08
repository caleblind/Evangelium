from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from . import views

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('missionary', views.MissionaryViewSet)

urlpatterns = [
   path('', include(router.urls))
]
