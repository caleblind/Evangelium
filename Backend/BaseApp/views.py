# Imports
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Missionary, Church, UserProfile
from .serializer import UserProfileSerializer
from rest_framework import viewsets, permissions

# Gets all church and missionary objects and renders the data on matching.html
@login_required
def matching(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   data = {
       'churches': church_data,
       'missionaries': missionary_data,
   }
   return render(request, 'matching.html', context=data)

@login_required
def home(request):
   return render(request,"matching.html")

def authView(request):
   if request.method =="POST":
      form = UserCreationForm(request.POST or None)
      if form.is_valid():
         form.save()
         return redirect("/accounts/login/")
   else:
      form = UserCreationForm()
   return render(request, "registration/signup.html",{"form": form})

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Allow users to view other profiles
        return UserProfile.objects.all()

    def get_object(self):
        # Retrieve user's own profile
        return self.request.user.profile