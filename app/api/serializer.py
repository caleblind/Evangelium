from rest_framework import serializers
from .models import Missionary, Church

#Serializer class for missionaries
class MissionarySerializer(serializers.ModelSerializer):
   class Meta:
      model = Missionary
      fields = ('MissionaryName', 'MissionaryField')

#Serializer class for churhes
class ChurchSerializer(serializers.ModelSerializer):
   class Meta:
      model = Church
      fields = ('ChurchName', 'ChurchLocation')



   