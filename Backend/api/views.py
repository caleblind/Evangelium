from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from BaseApp.models import Profile, Tag
from BaseApp.serializer import ProfileSerializer
import logging

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