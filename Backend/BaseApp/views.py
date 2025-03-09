import logging
from rest_framework import generics, filters, views, response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.exceptions import FieldError
from django.db.utils import DatabaseError
from .models import (
   Tag,
   SearchHistory,
   ExternalMedia,
   Profile
)
from .serializer import (
   TagSerializer,
   SeachHistorySerializer,
   ExternalMediaSerializer,
   ProfileSerializer
)


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
   permission_classes = [IsAuthenticated]  # Only authenticated users can access

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

      # Find profiles with at least one matching tag, excluding current user
      matching_profiles = (
         Profile.objects.filter(Q(tags__in=user_tags))
         .exclude(user=self.request.user)
         .distinct()
      )

      return matching_profiles.exclude(user_type=user_profile.user_type)


class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name', 'tag_description', 'tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [AllowAny]


class SearchHistoryViewSet(ModelViewSet):
   queryset = SearchHistory.objects.all()
   serializer_class = SeachHistorySerializer
   permission_classes = [AllowAny]


class ExternalMediaViewSet(ModelViewSet):
   queryset = ExternalMedia.objects.all()
   serializer_class = ExternalMediaSerializer
   permission_classes = [AllowAny]


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
      name = request.GET.get('name', '').strip()
      user_type = request.GET.get('user_type', '').strip()
      denomination = request.GET.get('denomination', '').strip()
      city = request.GET.get('city', '').strip()
      state = request.GET.get('state', '').strip()
      country = request.GET.get('country', '').strip()
      description = request.GET.get('description', '').strip()
      tags = request.GET.getlist('tags', [])

      queryset = (
         Profile.objects.select_related('user')
         .prefetch_related('tags')
         .all()
      )

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

      if description:
         queryset = queryset.filter(description__icontains=description)

      if city:
         queryset = queryset.filter(city__icontains=city)

      if state:
         queryset = queryset.filter(state__icontains=state)

      if country:
         queryset = queryset.filter(country__icontains=country)

      for tag in tags:
         queryset = queryset.filter(tags__id=tag)

      queryset = queryset.distinct()

      serializer = ProfileSerializer(queryset, many=True)
      return Response({
         'results': serializer.data,
         'count': queryset.count()
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
   except DatabaseError as e:
      logger.error("Database error in detailed_search: %s", str(e))
      return Response(
         {
            'error': 'Database error occurred',
            'detail': 'An error occurred while accessing the database'
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
