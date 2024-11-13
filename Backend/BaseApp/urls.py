from django.urls import path, include
from rest_framework import routers
from .views import LoginView, UserViewSet, SupporterViewSet,\
                   MissionaryViewSet, TagViewSet, TagRecordViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet, broke_login,\
                   LogoutView

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
   path('login/', LoginView.as_view(), name="login"),
   path('logout/', LogoutView.as_view(), name="logout"),
   path('broke/', broke_login, name="broke")
]
