from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework import generics, filters
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

class ProfileListCreateView(generics.ListCreateAPIView):
   serializer_class = ProfileSerializer
   permission_classes = [IsAuthenticated]  # Requires login to access
   filter_backends = [filters.SearchFilter]
   search_fields = ['user_type', 'city', 'state', 'country', 'denomination']
   filterset_fields = ['user_type', 'city', 'state', 'country', 'denomination', 'tags']

   def get_queryset(self):
      """
      If 'me' is in the URL, return only the current user's profile.
      Otherwise, return all profiles.
      """
      request = self.request
      if request.parser_context and 'me' in request.parser_context['kwargs']:
         return Profile.objects.filter(user=request.user)  # Only return the logged-in user's profile
      return Profile.objects.select_related('user').prefetch_related('tags').all()

   def perform_create(self, serializer):
      """
      Assigns the logged-in user to the profile upon creation.
      """
      serializer.save(user=self.request.user)

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Profile.objects.select_related('user').all()
   serializer_class = ProfileSerializer
   permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Authenticated users, but only owner or admin can edit

class CurrentUserProfileView(APIView):
   """
   Handles retrieving the logged-in user's profile.
   """
   permission_classes = [IsAuthenticated]

   def get(self, request):
      """
      Returns the authenticated user's profile.
      """
      profile = get_object_or_404(Profile, user=request.user)
      serializer = ProfileSerializer(profile)
      return Response(serializer.data)

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
