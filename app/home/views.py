from django.shortcuts import render

#Import a Http Response
from django.http import HttpResponse

#This function returns the reponse 'Hello World' when a request is sent to this function
def home(request):
   return HttpResponse('Hello World!')
