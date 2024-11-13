from django.contrib import admin

# Register your models here.
from .models import Missionary, Supporter, User

# Registering tables into admin/
admin.site.register(Missionary)
admin.site.register(Supporter)
admin.site.register(User)
