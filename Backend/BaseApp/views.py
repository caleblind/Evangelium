from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile
from .serializer import TagSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer,\
                        ProfileSerializer

class IsOwnerOrAdmin(BasePermission):
   """
   Custom permission to allow only the profile owner or an admin to edit.
   """
   def has_object_permission(self, request, view, obj):
      return request.user == obj.user or request.user.is_staff  # Owner or Admin

class CurrentUserProfileView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
      """Retrieve the profile of the currently authenticated user."""
      profile = get_object_or_404(Profile, user=request.user)
      serializer = ProfileSerializer(profile)
      return Response(serializer.data)

class ProfileListCreateView(generics.ListCreateAPIView):
   queryset = Profile.objects.select_related(
      'user').prefetch_related('tags').all()
   serializer_class = ProfileSerializer
   permission_classes = [IsAuthenticated]
   filter_backends = [filters.SearchFilter]
   search_fields = ['user_type', 'city', 'state', 'country', 'denomination']
   filterset_fields = ['user_type', 'city', 'state', 'country',
                       'denomination', 'tags']

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Profile.objects.select_related('user').all()
   serializer_class = ProfileSerializer
   permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Authenticated users, but only owner or admin can edit

# Tag viewset that performs CRUD operations
class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name','tag_description','tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [AllowAny]

# Search history viewset that performs CRUD operations
class SearchHistoryViewSet(ModelViewSet):
   queryset = SearchHistory.objects.all()
   serializer_class = SeachHistorySerializer
   permission_classes = [AllowAny]

# External media viewset that performs CRUD operations
class ExternalMediaViewSet(ModelViewSet):
   queryset = ExternalMedia.objects.all()
   serializer_class = ExternalMediaSerializer
   permission_classes = [AllowAny]
