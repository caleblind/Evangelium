from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile, ProfileTagging
from .serializer import TagSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer,\
                        ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction

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

      return matching_profiles

# Tag viewset that performs CRUD operations
class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name','tag_description','tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [IsAuthenticated]

   def create(self, request, *args, **kwargs):
      tag_name = request.data.get('tag_name')
      
      # Handle predefined tag creation (admin only)
      if request.data.get('tag_is_predefined', False):
         if not request.user.is_staff:
            return Response({
               'error': 'Only administrators can create predefined tags'
            }, status=status.HTTP_403_FORBIDDEN)
         return super().create(request, *args, **kwargs)
      
      # Create a new tag
      serializer = self.get_serializer(data={
         'tag_name': tag_name,
         'tag_description': request.data.get('tag_description', ''),
         'tag_is_predefined': False
      })
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      
      return Response(serializer.data, status=status.HTTP_201_CREATED)

# View for adding tags to other profiles
class AddTagToProfileView(generics.CreateAPIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]

   def create(self, request, *args, **kwargs):
      profile_id = request.data.get('profile_id')
      tag_name = request.data.get('tag_name')
      
      if not profile_id:
         return Response({
            'error': 'profile_id is required'
         }, status=status.HTTP_400_BAD_REQUEST)
      
      try:
         with transaction.atomic():
            profile = Profile.objects.get(user_id=profile_id)
            
            # Try to get existing tag first
            tag = Tag.objects.filter(tag_name=tag_name).first()
            
            if not tag:
               # Create new tag
               tag = Tag.objects.create(
                  tag_name=tag_name,
                  tag_description=request.data.get('tag_description', ''),
                  tag_is_predefined=False
               )
            
            # Create the profile-tag relationship with metadata
            ProfileTagging.objects.create(
               profile=profile,
               tag=tag,
               added_by=request.user
            )
            
            return Response({
               'message': f'Tag "{tag_name}" added to profile successfully',
               'tag_id': tag.id,
               'profile_id': profile_id,
               'added_by': request.user.id
            }, status=status.HTTP_200_OK)
         
      except Profile.DoesNotExist:
         return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
         )
      except IntegrityError:
         return Response({
            'error': 'You have already added this tag to this profile'
         }, status=status.HTTP_400_BAD_REQUEST)

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
