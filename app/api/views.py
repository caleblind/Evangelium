# Imports
from django.contrib.auth import authenticate, login as django_login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Missionary, Church

# Gets all missionary objects and renders the data on missionaries.html
def missionaries(request):
   missionary_data = Missionary.objects.all()
   context = {'missionaries': missionary_data}
   return render(request, 'missionaries.html', context)

# Gets all church objects and renders the data on churches.html
def churches(request):
   church_data = Church.objects.all()
   context = {'churches': church_data}
   return render(request, 'churches.html', context)

# Gets all church and missionary objects and renders the data on users.html
def users(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   user_data = {
       'churches': church_data,
       'missionaries': missionary_data,
   }
   return render(request, 'users.html', user_data)

# Gets all church and missionary objects and renders the data on matching.html
def matching(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   data = {
       'churches': church_data,
       'missionaries': missionary_data,
   }
   return render(request, 'matching.html', context=data)

# Gets all user objects and renders the data on connections_list.html
def connections_list(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   data = {
       'churches': church_data,
       'missionaries': missionary_data,
   }
   return render(request, 'connections_list.html', context=data)

# Django_login page
def login(request):
   if request.user.is_authenticated:
      return redirect('connections_list')

   if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      user = authenticate(request, username=email, password=password)

      if user is not None:
         django_login(request, user)
         return redirect('connections_list')
      messages.error(request, 'Invalid email or password.')

   return render(request, 'login.html')

# Logout button that redirects to login page
def logout_view(request):
   logout(request)
   return redirect('login')

@login_required
def home(request):
   return render(request,"home.html")

def authView(request):
   if request.method =="POST":
      form = UserCreationForm(request.POST or None)
      if form.is_valid():
         form.save()
   else:
      form = UserCreationForm()
   return render(request, "registration/signup.html",{"form": form})