from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Profile, Tag, TagRecord, SearchHistory,\
                    ExternalMedia
from .serializer import TagSerializer,\
                        TagRecordSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer, LoginSerializer
from django.http import HttpResponse 

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

# API view for validating user login
@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
   serializer_class = LoginSerializer
   permission_classes = [AllowAny]
   authentication_classes = [SessionAuthentication]

   # Logs user in and creates a session
   def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
         user = serializer.validated_data
         login(request, user)
         return Response({'message':'login successful'},
                         status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout API view
class LogoutView(APIView):
   permission_classes = [AllowAny]
   def post(self, request):
      logout(request)
      return Response({'message':'logout successful'},
                      status=status.HTTP_200_OK)

# Tag endpoint
@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def tags_api(request):

   if request.method == "GET":
      tags = Tag.objects.order_by("id")
      return HttpResponse(list(tags))

   elif request.method == 'POST': 
      data = JSONParser().parse(request)
      serializer = TagSerializer(data=data)
      if serializer.is_valid(): 
         serializer.save() 
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response({"error": "Invalid tag"}, status=status.HTTP_400_BAD_REQUEST)

   return HttpResponse({"error": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)