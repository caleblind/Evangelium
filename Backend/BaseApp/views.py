from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile
from .serializer import TagSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer,\
                        ProfileSerializer

class ProfileListCreateView(generics.ListCreateAPIView):
   queryset = Profile.objects.select_related(
      'user').prefetch_related('tags').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing
   filter_backends = [filters.SearchFilter]
   search_fields = ['user_type', 'city', 'state', 'country', 'denomination']
   filterset_fields = ['user_type', 'city', 'state', 'country',
                       'denomination', 'tags']

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Profile.objects.select_related('user').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing

class MatchmakingResultsView(generics.ListAPIView):
   serializer_class = ProfileSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]  # Only authenticated users can access

   def get_queryset(self):
      user_profile = Profile.objects.filter(
         user=self.request.user).prefetch_related('tags').first()

      if not user_profile:
         return Profile.objects.none()
         # Return an empty queryset if the user has no profile

      # Get the tags associated with the current user's profile
      user_tags = user_profile.tags.all()

      # Find profiles with at least one matching tag, excluding
      # the current user's profile
      matching_profiles = Profile.objects.filter(
         Q(tags__in=user_tags)).exclude(
            user=self.request.user).distinct()

      return matching_profiles.exclude(user_type=user_profile.user_type)

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
