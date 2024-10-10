from django.db import models

# User Models
class Missionary(models.Model):
   MissionaryName = models.CharField()
   MissionaryField = models.CharField()

class Church(models.Model):
   ChurchName = models.CharField()
   ChurchLocation = models.IntegerField()