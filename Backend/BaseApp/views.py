from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, filters
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile
from .serializer import TagSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer,\
                        ProfileSerializer, UserSerializer

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

# User viewset that performs CRUD operations
class UserViewSet(ModelViewSet):
   filterset_fields = ['user_type','description','phone_number']
   serializer_class = UserSerializer
   queryset = User.objects.all()
   permission_classes = [AllowAny]

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

# Logout API view
class LogoutView(APIView):
   permission_classes = [AllowAny]
   def post(self, request):
      logout(request)
      return Response({'message':'logout successful'},
                      status=status.HTTP_200_OK)

class SimilarUsersView(generics.ListAPIView):
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]

   def get_queryset(self):
      user = self.request.user

      # Get the tags associated with the logged in user
      user_tags = user.profile.tags.all()

      # Find users who share at least one tag with the logged-in user
      similar_users = Profile.objects.filter(tags__in=user_tags).distinct()

      # Exclude the logged-in user from the result
      return similar_users.exclude(user=user)
