from django.urls import path, include

# Imports all views from view.py
from . import views


urlpatterns = [
   path('missionaries/', views.missionaries, name='missionaries'),
   path('churches/', views.churches, name='churches'),
   path('users/', views.users, name='users'),
   path('matching/', views.matching, name='matching'),
   path('login/', views.login, name='login'),
   path('connections_list/', views.connections_list, name='connections_list'),
   path('connections/', views.connections_list, name='connections_list'),
   path('logout/', views.logout_view, name='logout'),
   path("signup/", views.authView, name ="authView"),
   path("accounts/", include("django.contrib.auth.urls")),
]
