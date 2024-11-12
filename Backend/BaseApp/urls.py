from django.urls import path, include
from rest_framework import routers
from .views import LoginAPIView, UserViewSet, SupporterViewSet,\
                   MissionaryViewSet, TagViewSet, TagRecordViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('supporter', SupporterViewSet)
router.register('missionary', MissionaryViewSet)
router.register('tag', TagViewSet)
router.register('tagrecord', TagRecordViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', LoginAPIView.as_view(), name="login"),
]
