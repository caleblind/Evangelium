import logging
from rest_framework import generics, filters, views, response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import DatabaseError
from django.core.exceptions import FieldError
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment
from .serializer import TagSerializer, SearchHistorySerializer, \
    ExternalMediaSerializer, \
    ProfileSerializer, ProfileVoteSerializer, ProfileCommentSerializer

class ProfileListCreateView(generics.ListCreateAPIView):
   queryset = Profile.objects.select_related(
      'user').prefetch_related('tags').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing
   filter_backends = [filters.SearchFilter]
   search_fields = [
      'user_type',
      'city',
      'state',
      'country',
      'denomination'
   ]
   filterset_fields = [
      'user_type',
      'city',
      'state',
      'country',
      'denomination',
      'tags'
   ]



class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Profile.objects.select_related('user').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing


class MatchmakingResultsView(generics.ListAPIView):
   serializer_class = ProfileSerializer
   authentication_classes = [JWTAuthentication]
   # Only authenticated users can access
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
      user_profile = (
         Profile.objects.filter(user=self.request.user)
         .prefetch_related('tags')
         .first()
      )

      if not user_profile:
         return Profile.objects.none()

      # Get the tags associated with the current user's profile
      user_tags = user_profile.tags.all()

      # Find profiles with at least one matching tag, excluding
      # the current user's profile
      matching_profiles = Profile.objects.filter(
         Q(tags__in=user_tags)).exclude(
          user=self.request.user).distinct()

      return matching_profiles.exclude(user_type=user_profile.user_type)

class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name', 'tag_description', 'tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [AllowAny]

# Search history viewset that performs CRUD operations
class SearchHistoryViewSet(ModelViewSet):
   queryset = SearchHistory.objects.all()
   serializer_class = SearchHistorySerializer
   permission_classes = [AllowAny]

# External media viewset that performs CRUD operations
class ExternalMediaViewSet(ModelViewSet):
   queryset = ExternalMedia.objects.all()
   serializer_class = ExternalMediaSerializer
   permission_classes = [AllowAny]

# View for retrieving the currently logged in user
class CurrentUserView(views.APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request):
      user_profile = (
         Profile.objects.filter(user=request.user)
         .select_related('user')
         .prefetch_related('tags')
         .first()
      )

      if user_profile:
         serializer = ProfileSerializer(user_profile)
         return response.Response(serializer.data)

      return response.Response({"error": "Profile not found"}, status=404)

class ProfileVoteView(generics.CreateAPIView, generics.UpdateAPIView):
   serializer_class = ProfileVoteSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def create(self, request, *args, **kwargs):
      profile_id = request.data.get('profile')
      is_upvote = request.data.get('is_upvote')

      # Check if vote already exists
      existing_vote = ProfileVote.objects.filter(
          voter=request.user,
          profile_id=profile_id
      ).first()

      if existing_vote:
         # Update existing vote
         existing_vote.is_upvote = is_upvote
         existing_vote.save()
         serializer = self.get_serializer(existing_vote)
         return response.Response(serializer.data)

      # Create new vote
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileCommentView(generics.CreateAPIView, generics.UpdateAPIView):
   serializer_class = ProfileCommentSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]
   queryset = ProfileComment.objects.all()

   def create(self, request, *args, **kwargs):
      # Check if user has already commented
      profile_id = request.data.get('profile')
      existing_comment = ProfileComment.objects.filter(
          commenter=request.user,
          profile_id=profile_id
      ).exists()

      if existing_comment:
         return response.Response(
             {"error": "You have already commented on this profile"},
             status=status.HTTP_400_BAD_REQUEST
         )

      # Check if user has voted
      has_voted = ProfileVote.objects.filter(
          voter=request.user,
          profile_id=profile_id
      ).exists()

      if not has_voted:
         return response.Response(
             {"error": "You must vote before commenting"},
             status=status.HTTP_400_BAD_REQUEST
         )

      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return response.Response(serializer.data, status=status.HTTP_201_CREATED)

   def update(self, request, *args, **kwargs):
      comment = self.get_object()

      # Check if the user is the owner of the comment
      if comment.commenter != request.user:
         return response.Response(
             {"error": "You can only edit your own comments"},
             status=status.HTTP_403_FORBIDDEN
         )

      serializer = self.get_serializer(
         comment, data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)

      return response.Response(serializer.data)

   def perform_create(self, serializer):
      serializer.save(commenter=self.request.user)


class ProfileVoteStatusView(views.APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request, profile_id):
      vote = ProfileVote.objects.filter(
          voter=request.user,
          profile_id=profile_id
      ).first()

      return response.Response({
          'has_voted': vote is not None,
          'is_upvote': vote.is_upvote if vote else None
      })

logger = logging.getLogger(__name__)


@api_view(['GET'])
def search_profiles(request):
   """Search profiles with filtering capabilities."""
   query = request.GET.get('q', '')
   profile_type = request.GET.get('type', '')
   denomination = request.GET.get('denomination', '')
   mission_field = request.GET.get('missionField', '')

   logger.info(
      "Search request - Query: %s, Type: %s, Denomination: %s, Field: %s",
      query,
      profile_type,
      denomination,
      mission_field
   )

   try:
      profiles = (
         Profile.objects.select_related('user')
         .prefetch_related('tags')
         .all()
      )
      logger.debug("Initial profile count: %d", profiles.count())

      if profile_type:
         if profile_type == 'supporter':
            profiles = profiles.filter(user_type='supporter')
         elif profile_type == 'missionary':
            profiles = profiles.filter(user_type='missionary')
      logger.debug("After type filter count: %d", profiles.count())

      if query:
         profiles = profiles.filter(
            Q(user__username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(country__icontains=query) |
            Q(tags__tag_name__icontains=query) |  # Search in tag names
            Q(denomination__icontains=query)  # Search in denomination
         ).distinct()  # Add distinct to avoid duplicates
         logger.debug("After text search count: %d", profiles.count())

      if denomination:
         profiles = profiles.filter(denomination__iexact=denomination)
         logger.debug("After denomination filter count: %d", profiles.count())

      if mission_field:
         profiles = (
            profiles.filter(tags__tag_name__iexact=mission_field)
            .distinct()
         )
         logger.debug("After mission field filter count: %d", profiles.count())

      serializer = ProfileSerializer(profiles, many=True)
      result_data = serializer.data
      logger.info("Returning %d results", len(result_data))

      return Response({
         'results': result_data,
         'total': len(result_data)
      })

   except ValidationError as e:
      logger.error("Validation error in search_profiles: %s", str(e))
      return Response(
         {
            'error': 'Invalid search parameters',
            'detail': str(e)
         },
         status=400
      )
   except FieldError as e:
      logger.error("Field error in search_profiles: %s", str(e))
      return Response(
         {
            'error': 'Invalid field in search query',
            'detail': str(e)
         },
         status=400
      )
   except DatabaseError as e:
      logger.error("Database error in search_profiles: %s", str(e))
      return Response(
         {
            'error': 'Database error occurred',
            'detail': 'An error occurred while accessing the database'
         },
         status=500
      )


@api_view(['GET'])
def detailed_search(request):
   """Advanced search endpoint with AND logic for all criteria."""
   try:
      # Log all request parameters for debugging
      logger.info("Detailed search request parameters: %s", request.GET)

      name = request.GET.get('name', '').strip()
      user_type = request.GET.get('user_type', '').strip()
      denomination = request.GET.get('denomination', '').strip()
      city = request.GET.get('city', '').strip()
      state = request.GET.get('state', '').strip()
      country = request.GET.get('country', '').strip()
      description = request.GET.get('description', '').strip()
      tags = request.GET.getlist('tags', [])

      # Log processed parameters
      logger.info(
         "Processed parameters - Name: %s, Type: %s, Denomination: %s, City: %s, State: %s, Country: %s, Tags: %s",
         name,
         user_type,
         denomination,
         city,
         state,
         country,
         tags
      )

      queryset = (
         Profile.objects.select_related('user')
         .prefetch_related('tags')
         .all()
      )
      logger.debug("Initial profile count: %d", queryset.count())

      if name:
         queryset = queryset.filter(
            Q(first_name__icontains=name) |
            Q(last_name__icontains=name) |
            Q(user__username__icontains=name)
         )
         logger.debug("After name filter count: %d", queryset.count())

      if user_type:
         logger.debug("Applying user_type filter with value: %s", user_type)
         queryset = queryset.filter(user_type__iexact=user_type)
         logger.debug("After user_type filter count: %d", queryset.count())

      if denomination:
         queryset = queryset.filter(denomination__iexact=denomination)
         logger.debug("After denomination filter count: %d", queryset.count())

      if description:
         queryset = queryset.filter(description__icontains=description)
         logger.debug("After description filter count: %d", queryset.count())

      if city:
         queryset = queryset.filter(city__icontains=city)
         logger.debug("After city filter count: %d", queryset.count())

      if state:
         queryset = queryset.filter(state__icontains=state)
         logger.debug("After state filter count: %d", queryset.count())

      if country:
         queryset = queryset.filter(country__icontains=country)
         logger.debug("After country filter count: %d", queryset.count())

      try:
         for tag in tags:
            logger.debug("Processing tag: %s (type: %s)", tag, type(tag))
            queryset = queryset.filter(tags__id=tag)
            logger.debug("After tag %s filter count: %d", tag, queryset.count())
      except ValueError as e:
         logger.error("Invalid tag value: %s", str(e))
         return Response(
            {
               'error': 'Invalid tag value',
               'detail': str(e)
            },
            status=400
         )
      except Exception as e:
         logger.error("Error processing tags: %s", str(e))
         return Response(
            {
               'error': 'Error processing tags',
               'detail': str(e)
            },
            status=400
         )

      queryset = queryset.distinct()
      logger.debug("Final profile count: %d", queryset.count())

      serializer = ProfileSerializer(queryset, many=True)
      return Response({
         'results': serializer.data,
         'total': queryset.count()
      })

   except ValidationError as e:
      logger.error("Validation error in detailed_search: %s", str(e))
      return Response(
         {
            'error': 'Invalid search parameters',
            'detail': str(e)
         },
         status=400
      )
   except FieldError as e:
      logger.error("Field error in detailed_search: %s", str(e))
      return Response(
         {
            'error': 'Invalid field in search query',
            'detail': str(e)
         },
         status=400
      )
   except Exception as e:
      logger.error("Unexpected error in detailed_search: %s", str(e), exc_info=True)
      return Response(
         {
            'error': 'An unexpected error occurred',
            'detail': str(e)
         },
         status=500
      )


@api_view(['GET'])
def get_unique_denominations(_):
   """Get all unique denominations from profiles."""
   try:
      denominations = (
         Profile.objects.exclude(denomination__isnull=True)
         .exclude(denomination__exact='')
         .values_list('denomination', flat=True)
         .distinct()
         .order_by('denomination')
      )
      return Response({
         'denominations': list(denominations)
      })
   except DatabaseError as e:
      logger.error("Database error in get_unique_denominations: %s", str(e))
      return Response(
         {
            'error': 'Database error occurred',
            'detail': 'An error occurred while accessing the database'
         },
         status=500
      )
