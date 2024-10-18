from django.shortcuts import render

#My imports (don't exactly know what all these do)
from .models                 import Missionary, Church
from .serializer             import MissionarySerializer, ChurchSerializer
from rest_framework          import generics, status, mixins
from django.http             import JsonResponse, HttpResponse
from rest_framework.parsers  import JSONParser
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView

#Generic Missionary List, Create View
class Missionary_LC_view(generics.ListCreateAPIView):
   queryset         = Missionary.objects.all()
   serializer_class = MissionarySerializer

   #Overrides generic API views
   def delete(self, request, *args, **kwargs):
      Missionary.objects.all().delete()
      return Response(status = status.HTTP_204_NO_CONTENT)

#Generic Missionary Retrieve, Update, Destroy View
class Missionary_RUD_view(generics.RetrieveUpdateDestroyAPIView):
   queryset         = Missionary.objects.all()
   serializer_class = MissionarySerializer
   lookup_field     = "pk"
   
#Generic Church List, Create View
class Church_LC_view(generics.ListCreateAPIView):
   queryset         = Church.objects.all()
   serializer_class = ChurchSerializer

   #Overrides generic API views
   def delete(self, request, *args, **kwargs):
      Church.objects.all().delete()
      return Response(status = status.HTTP_204_NO_CONTENT)

#Generic Church Retrieve, Update, Destroy View
class Church_RUD_view(generics.RetrieveUpdateDestroyAPIView):
   queryset         = Church.objects.all()
   serializer_class = ChurchSerializer
   lookup_field     = "pk"