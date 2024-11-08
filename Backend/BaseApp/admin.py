from django.contrib import admin

# Register your models here.
from .models import Missionary, Supporter

#Registering tables into admin/
admin.site.register(Missionary)
admin.site.register(Supporter)
