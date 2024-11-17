from django.urls import path, include
from rest_framework import routers
from .views import LoginView, UserViewSet, SupporterViewSet,\
                   MissionaryViewSet, TagViewSet, TagRecordViewSet,\
                   SearchHistoryViewSet, ExternalMediaViewSet,\
                   LogoutView, RegistrationView, UserDetailView

from . import views

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
   path('register/', RegistrationView.as_view(), name="register"),
   path('userdetail/<int:pk>/', UserDetailView.as_view(), name="userdetail"),

   path('api/test_get/', views.test_get, name='test_get'),
   path('api/test_post/', views.test_post, name='test_post'),
]
