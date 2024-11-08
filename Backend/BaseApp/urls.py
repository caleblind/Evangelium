from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from . import views

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('supporter', views.SupporterViewSet)
router.register('missionary', views.MissionaryViewSet)
router.register('tag', views.TagViewSet)
router.register('tagrecord', views.TagRecordViewSet)
router.register('searchhistory', views.SearchHistoryViewSet)
router.register('externalmedia', views.ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls))
]
