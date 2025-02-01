from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt import tokens
from .models import Profile, Tag, TagRecord, SearchHistory,\
                    ExternalMedia
from .serializer import TagSerializer,\
                        TagRecordSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer

# User viewset that performs CRUD operations
class UserViewSet(ModelViewSet):
   filterset_fields = ['user_type','description','phone_number']
   queryset = User.objects.all()
   permission_classes = [AllowAny]

# Tag viewset that performs CRUD operations
class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name','tag_description','tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [AllowAny]

# Tag record viewset that performs CRUD operations
class TagRecordViewSet(ModelViewSet):
   filterset_fields = ['tag','user','added_date']
   queryset = TagRecord.objects.all()
   serializer_class = TagRecordSerializer
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

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)

# Logout API view
class LogoutView(APIView):
   permission_classes = [AllowAny]
   def post(self, request):
      logout(request)
      return Response({'message':'logout successful'},
                      status=status.HTTP_200_OK)
