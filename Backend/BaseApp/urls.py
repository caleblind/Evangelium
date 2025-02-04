from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, TagViewSet, TagRecordViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet,\
                   LogoutView

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('tag', TagViewSet)
router.register('tagrecord', TagRecordViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)
#router.register('login/', login_view)

urlpatterns = [
   path('', include(router.urls)),
   path('logout/', LogoutView.as_view(), name="logout"),
]
