from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django.contrib.auth import login, logout #get_user_model
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Tag, TagRecord, SearchHistory,\
                    ExternalMedia
from .serializer import TagSerializer,\
                        TagRecordSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer, LoginSerializer,\
                        RegistrationSerializer

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


@api_view(['POST'])
@permission_classes((AllowAny,))
def RegistrationView(request):
   if request.method == 'POST':
      # Initialize serializer with data from the request
      serializer = RegistrationSerializer(data = request.data)
      # Validate and create the user
      if serializer.is_valid():
         # This will create both user and profile separately
         user = serializer.save()
         return Response({
            'message': 'User created successfully',
            'user': {
               'username': user.username,
               'email': user.email,
               'first_name': user.first_name,
               'last_name': user.last_name
            }
         }, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   return Response({'detail': 'Method not allowed'},
                   status=status.HTTP_405_METHOD_NOT_ALLOWED)
