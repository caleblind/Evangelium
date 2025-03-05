from django.urls import path
from api.views import search_profiles

urlpatterns = [
    # ... existing urls ...
    path('profiles/search/', search_profiles, name='search-profiles'),
] 