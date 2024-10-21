from django.urls import path, include
from django.contrib.auth import views as auth_views

#Imports all views from view.py
from . import views


urlpatterns = [
   path('missionaries/', views.missionaries, name = 'missionaries'),
   path('churches/', views.churches, name = 'churches'),
   path('users/', views.users, name = 'users'),
   path('connections_list/', views.connections_list, name = 'connections_list'),

   path('matching/', views.matching, name = 'matching'),
   path('login/', views.login, name='login'),
   path('signup/', views.signup, name='signup'),  # Optional for registration
   path('connections/', views.connections_list, name='connections_list'),
   path('logout/', views.logout_view, name='logout'),

# Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

