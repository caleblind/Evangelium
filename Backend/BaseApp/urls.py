from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from . import views

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('missionary', views.UserViewSet)
router.register('missionary', views.SupporterViewSet)
router.register('missionary', views.MissionaryViewSet)
router.register('missionary', views.TagViewSet)
router.register('missionary', views.TagRecordViewSet)
router.register('missionary', views.SearchHistoryViewSet)
router.register('missionary', views.ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls))
]
