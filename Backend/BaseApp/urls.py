from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, TagViewSet, TagRecordViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet,\
                   LogoutView, ProfileListCreateView, ProfileDetailView,\
                   SimilarUsersView, RegistrationView

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
   path('api/profiles/', ProfileListCreateView.as_view(),
        name='profile-list-create'),
   path('api/profiles/<int:pk>/', ProfileDetailView.as_view(),
        name='profile-detail'),
   path('similar-users/', SimilarUsersView.as_view(), name='similar-users'),
   path('registration/', RegistrationView, name="registration")
]
