from django.contrib import admin

# Register your models here.
from .models import Missionary, Church

#Registering tables into admin/
admin.site.register(Missionary)
admin.site.register(Church)
