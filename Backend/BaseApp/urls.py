from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, SearchHistoryViewSet,\
                   ExternalMediaViewSet,\
                   ProfileListCreateView, ProfileDetailView, CurrentUserProfileView

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('tag', TagViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('api/profiles/', ProfileListCreateView.as_view(),
        name='profile-list-create'),
   path('api/profiles/me/', CurrentUserProfileView.as_view(),
        name='current-user-profile'),  # Uses same view
   path('api/profiles/<int:pk>/', ProfileDetailView.as_view(),
        name='profile-detail'),
]
