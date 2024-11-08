from rest_framework.viewsets import ModelViewSet
#from rest_framework.decorators import api_view, permission_classes, authentication_classes
#from django.contrib.auth import login, logout
#from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, Supporter, Missionary,\
                    Tag, TagRecord, SearchHistory,\
                    ExternalMedia
from .serializer import UserSerializer, SupporterSerializer,\
                        MissionarySerializer, TagSerializer,\
                        TagRecordSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer

# API viewset for Users that performs CRUD operations
class UserViewSet(ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [IsAuthenticated]

# API viewset for Supporters that performs CRUD operations
class SupporterViewSet(ModelViewSet):
   queryset = Supporter.objects.all()
   serializer_class = SupporterSerializer
   permission_classes = [IsAuthenticated]

# API viewset for Missionaries that performs CRUD operations
class MissionaryViewSet(ModelViewSet):
   queryset = Missionary.objects.all()
   serializer_class = MissionarySerializer
   permission_classes = [IsAuthenticated]

# API viewset for Tags that performs CRUD operations
class TagViewSet(ModelViewSet):
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [IsAuthenticated]

# API viewset for Tag Records that performs CRUD operations
class TagRecordViewSet(ModelViewSet):
   queryset = TagRecord.objects.all()
   serializer_class = TagRecordSerializer
   permission_classes = [IsAuthenticated]

# API viewset for Search History that performs CRUD operations
class SearchHistoryViewSet(ModelViewSet):
   queryset = SearchHistory.objects.all()
   serializer_class = SeachHistorySerializer
   permission_classes = [IsAuthenticated]

# API viewset for External Media that performs CRUD operations
class ExternalMediaViewSet(ModelViewSet):
   queryset = ExternalMedia.objects.all()
   serializer_class = ExternalMediaSerializer
   permission_classes = [IsAuthenticated]
