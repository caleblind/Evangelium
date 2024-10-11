from rest_framework import serializers
from .models import Missionary, Church

#Serializer class for missionaries
class MissionarySerializer(serializers.ModelSerializer):
   class Meta:
      model  = Missionary
      fields = ('missionary_name', 'email_address', 'phone_number')

#Serializer class for churhes
class ChurchSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Church
      fields = ('church', 'location', 'phone_number', 'email_address')



   