from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Defines missionary table
class Missionary(models.Model):
   missionary_name = models.CharField(max_length=100)
   email_address = models.CharField(max_length=100)
   phone_number = models.IntegerField()
   field_of_service = models.CharField(max_length=100)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Missionaries"

   # Returns the missionary name
   def __str__(self):
      return str(self.missionary_name)

# Defines the church table
class Church(models.Model):
   church_name = models.CharField(max_length=100)
   church_address = models.CharField(max_length=100)
   pastor_name = models.CharField(max_length=100)
   church_number = models.IntegerField()
   email_address = models.CharField(max_length=100)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Churches"

   # Returns church name
   def __str__(self):
      return str(self.church_name)

#Manager for custom user models
class UserManager(BaseUserManager):
   def create_user(self, email, password=None, **extra_fields):
      if not email:
         raise ValueError("The Email field must be set")
      email = self.normalize_email(email)
      user  = self.model(email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user