from django.urls import path, include

#Imports all views from view.py
from . import views

urlpatterns = [
   path('missionaries/', views.missionaries, name = 'missionaries'),
   path('churches/', views.churches, name = 'churches'),
   path('users/', views.users, name = 'users'),
   path('christian/', views.christian, name = 'christian'),

   path('login/', views.login_page, name='login_page'),
   path('signup/', views.signup_page, name='signup_page'),  # Optional for registration
   path('connections/', views.connections_list, name='connections_list'),
   path('logout/', views.logout_view, name='logout'),

]