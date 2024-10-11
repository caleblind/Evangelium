from django.db import models

# User Models
class Missionary(models.Model):
   missionary_name = models.CharField(max_length = 100)
   email_address   = models.CharField(max_length = 100)
   phone_number    = models.IntegerField()

   def __str__(self):
      return self.missionary_name
   

class Church(models.Model):
   church_name    = models.CharField(max_length = 100)
   location       = models.CharField(max_length = 100)
   phone_number   = models.IntegerField()
   email_address  = models.CharField(max_length = 100)

   def __str__(self):
      return self.church_name