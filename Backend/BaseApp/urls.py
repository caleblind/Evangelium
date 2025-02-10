from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, TagViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet,\
                   LogoutView, ProfileListCreateView, ProfileDetailView,\
                   SimilarUsersView

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('tag', TagViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('logout/', LogoutView.as_view(), name="logout"),
   path('api/profiles/', ProfileListCreateView.as_view(),
        name='profile-list-create'),
   path('api/profiles/<int:pk>/', ProfileDetailView.as_view(),
        name='profile-detail'),
   path('similar-users/', SimilarUsersView.as_view(), name='similar-users'),
]
