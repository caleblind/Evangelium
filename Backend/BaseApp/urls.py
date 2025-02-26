from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, SearchHistoryViewSet,\
                   ExternalMediaViewSet,\
                   ProfileListCreateView, ProfileDetailView,\
                   MatchmakingResultsView, CurrentUserView

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('tag', TagViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('api/profiles/', ProfileListCreateView.as_view(),
        name='profile-list-create'),
   path('api/profiles/<int:pk>/', ProfileDetailView.as_view(),
        name='profile-detail'),
   path('api/profiles/match', MatchmakingResultsView.as_view()),
   path('api/profiles/me/', CurrentUserView.as_view(),
        name='current-user'),
]
