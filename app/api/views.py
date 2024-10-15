from django.shortcuts import render

#My imports 
from .models                 import Missionary, Church
from .serializer             import MissionarySerializer, ChurchSerializer
from rest_framework          import generics, status, mixins, viewsets
from django.http             import JsonResponse, HttpResponse
from rest_framework.parsers  import JSONParser
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
import requests 
from rest_framework.decorators import api_view, renderer_classes

#Missionary List/Create Class
class Missionary_LC_view(generics.ListCreateAPIView):
   queryset         = Missionary.objects.all()
   serializer_class = MissionarySerializer
#Missionary View Set Class
class Missionary_view_set(viewsets.ModelViewSet):
   queryset         = Missionary.objects.all().order_by('missionary_name')
   serializer_class = MissionarySerializer
#Missionary Retrieve/Update/Destroy Class
class Missionary_RUD_view(generics.RetrieveUpdateDestroyAPIView):
   queryset         = Missionary.objects.all()
   serializer_class = MissionarySerializer
   lookup_field     = "pk"
   

#Church List/Create Class
class Church_LC_view(generics.ListCreateAPIView):
   queryset         = Church.objects.all()
   serializer_class = ChurchSerializer
#Church View Set Class
class Church_view_set(viewsets.ModelViewSet):
   queryset         = Church.objects.all().order_by('church_name')
   serializer_class = ChurchSerializer
#Church Retrieve/Update/Destroy View Class
class Church_RUD_view(generics.RetrieveUpdateDestroyAPIView):
   queryset         = Church.objects.all()
   serializer_class = ChurchSerializer
   lookup_field     = "pk"

def missionaries(request):
   response = requests.get('http://127.0.0.1:8000/missionary/') 
   data = response.json()
   return render(request, 'missionaries.html', {'data': data})

def churches(request):
   response = requests.get('http://127.0.0.1:8000/church/')
   data = response.json()
   return render(request, 'churches.html', {'data': data})

@api_view(('GET',))
def users(request):
   church_response = requests.get('http://127.0.0.1:8000/church/')
   church_data = church_response.json()
   missionary_response = requests.get('http://127.0.0.1:8000/missionary/') 
   missionary_data = missionary_response.json()
   user_data={
      'churches': church_data,
      'missionaries': missionary_data,
   }
   return render(request, 'users.html', {'user_data': user_data})