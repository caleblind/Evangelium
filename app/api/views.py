from django.shortcuts import render

#My imports 
from .models                 import Missionary, Church
from .serializer             import MissionarySerializer, ChurchSerializer
from django.http             import JsonResponse, HttpResponse
from rest_framework.parsers  import JSONParser
from rest_framework.response import Response
import requests 

def missionaries(request):
   missionary_data = Missionary.objects.all()
   context = {'missionaries': missionary_data}
   return render(request, 'missionaries.html', context)

def churches(request):
   church_data = Church.objects.all()
   context = {'churches': church_data}
   return render(request, 'churches.html', context)

def users(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   user_data={
      'churches': church_data,
      'missionaries': missionary_data,
   }
   return render(request, 'users.html', user_data)

def matching(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   data={
      'churches': church_data,
      'missionaries': missionary_data,
   }
   return render(request, 'matching.html', context = data)

def login(request):
   return render(request, 'login.html')