from django.shortcuts import render

#My imports (don't exactly know what all these do)
from .models                import Missionary, Church
from .serializer            import MissionarySerializer, ChurchSerializer
from rest_framework         import generics, status
#from django.http            import JsonResponse, HttpResponse
#from rest_framework.parsers import JSONParser

#Generic Missionary List, Create View
class Missionary_LC_view(generics.ListCreateAPIView):
   queryset   = Missionary.objects.all()
   serializer = MissionarySerializer

#Generic Missionary Retrieve, Update, Destroy View
#class Missionary_RUD_view(generics.RetrieveUpdateDestroyAPIView):
#   queryset   = Missionary.objects.all()
#   serializer = MissionarySerializer
   

#Generic Church List, Create View
class Church_LC_view(generics.ListCreateAPIView):
   queryset   = Church.objects.all()
   serializer = ChurchSerializer

#Generic Church Retrieve, Update, Destroy View
#class Church_LC_view(generics.RetrieveUpdateDestroyAPIView):
#   queryset   = Church.objects.all()
#   serializer = ChurchSerializer