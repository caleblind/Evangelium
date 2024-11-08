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

#Custom djnago user manager for custom django user model
class UserManager(BaseUserManager):

   #Handles user creation by ensuring email entry/normalization
   #and password hashing/normalization
   def create_user(self, email, password=None, **extra_fields):
      if not email:
         raise ValueError("The Email field must be set")
      email = self.normalize_email(email)
      user  = self.model(email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user

   #Handles superuser creation for admins (django admin page users)
   def create_superuser(self, email, password=None, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_super', True)
      if extra_fields.get("is_staff") is not True:
         raise ValueError("Superuser must have is_staff=True.")
      if extra_fields.get("is_superuser") is not True:
         raise ValueError("Superuser must have is_superuser=True.")

      return self.create_user(email, password, **extra_fields)

#Custom django user model
class User(AbstractBaseUser):
   email = models.EmailField(max_length=254, unique=True, null=False)
   password = models.CharField(max_length=128)
   user_type = models.CharField(max_length=15)
   profile_picture = models.URLField(max_length=225, null=True, blank=True)
   description = models.TextField(null=True, blank=True)
   phone_number = models.CharField(max_length=100, null=False)

   #Links the custom django user manager to this custom user
   objects = UserManager()
   USERNAME_FIELD = 'email'
