import logging
from rest_framework import generics, filters, views, response, decorators
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
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

# View for retrieving the currently logged in user
class CurrentUserView(views.APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request):
      # Fetch the user's profile in the same way as MatchmakingResultsView
      user_profile = Profile.objects.filter(
         user=request.user
      ).select_related('user').prefetch_related('tags').first()

      if user_profile:
         serializer = ProfileSerializer(user_profile)
         return response.Response(serializer.data)

      return response.Response({"error": "Profile not found"}, status=404)

logger = logging.getLogger(__name__)

@api_view(['GET'])
def search_profiles(request):
    """
    Search profiles with filtering capabilities for churches and missionaries
    """
    # Get query parameters
    query = request.GET.get('q', '')
    profile_type = request.GET.get('type', 'missionaries')
    denomination = request.GET.get('denomination', '')
    mission_field = request.GET.get('missionField', '')

    logger.info(f"Search request - Query: {query}, Type: {profile_type}, Denomination: {denomination}, Field: {mission_field}")

    try:
        # Start with all profiles
        profiles = Profile.objects.select_related('user').prefetch_related('tags').all()
        logger.debug(f"Initial profile count: {profiles.count()}")

        # Filter by type (this is always applied)
        if profile_type == 'churches':
            profiles = profiles.filter(user_type='other')  # Assuming churches are marked as 'other'
        elif profile_type == 'missionaries':
            profiles = profiles.filter(user_type='missionary')
        logger.debug(f"After type filter count: {profiles.count()}")

        # Apply text search if provided
        if query:
            profiles = profiles.filter(
                Q(user__username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query) |
                Q(country__icontains=query)
            )
            logger.debug(f"After text search count: {profiles.count()}")

        # Apply optional filters only if they are provided
        if denomination:
            profiles = profiles.filter(denomination__iexact=denomination)
            logger.debug(f"After denomination filter count: {profiles.count()}")

        if mission_field:
            profiles = profiles.filter(tags__tag_name__iexact=mission_field).distinct()
            logger.debug(f"After mission field filter count: {profiles.count()}")

        # Serialize and return the results
        serializer = ProfileSerializer(profiles, many=True)
        result_data = serializer.data
        logger.info(f"Returning {len(result_data)} results")

        return Response({
            'results': result_data,
            'total': len(result_data)
        })

    except Exception as e:
        logger.error(f"Error in search_profiles: {str(e)}")
        return Response({
            'error': 'An error occurred while searching profiles',
            'detail': str(e)
        }, status=500)

@api_view(['GET'])
def detailed_search(request):
    """
    Advanced search endpoint that combines all criteria with AND logic
    """
    try:
        # Get all query parameters
        name = request.GET.get('name', '').strip()
        user_type = request.GET.get('user_type', '').strip()
        denomination = request.GET.get('denomination', '').strip()
        city = request.GET.get('city', '').strip()
        state = request.GET.get('state', '').strip()
        country = request.GET.get('country', '').strip()
        tags = request.GET.getlist('tags', [])

        # Start with all profiles
        queryset = Profile.objects.select_related('user').prefetch_related('tags').all()

        # Apply filters using AND logic
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name) |
                Q(user__username__icontains=name)
            )

        if user_type:
            queryset = queryset.filter(user_type__iexact=user_type)

        if denomination:
            queryset = queryset.filter(denomination__iexact=denomination)

        if city:
            queryset = queryset.filter(city__icontains=city)

        if state:
            queryset = queryset.filter(state__icontains=state)

        if country:
            queryset = queryset.filter(country__icontains=country)

        # Apply tag filters with AND logic
        for tag in tags:
            queryset = queryset.filter(tags__id=tag)

        # Ensure distinct results
        queryset = queryset.distinct()

        # Serialize the results
        serializer = ProfileSerializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'count': queryset.count()
        })

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500) 