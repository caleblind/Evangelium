from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics, filters
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
