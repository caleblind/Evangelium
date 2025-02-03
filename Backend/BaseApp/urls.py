from django.urls import path, include
from rest_framework import routers
from .views import LoginView, UserViewSet, TagViewSet, TagRecordViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet,\
                   LogoutView, tags_api

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('tag', TagViewSet)
router.register('tagrecord', TagRecordViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', LoginView.as_view(), name="login"),
   path('logout/', LogoutView.as_view(), name="logout"),
   path('tags/', tags_api, name="tags"),
]
