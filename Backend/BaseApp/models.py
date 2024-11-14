from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                       PermissionsMixin

# Custom djnago user manager for custom django user model
class UserManager(BaseUserManager):

   # Handles user creation by ensuring email entry/normalization
   # and password hashing/normalization
   def create_user(self, email, password=None, **extra_fields):
      if not email:
         raise ValueError("The Email field must be set")
      email = self.normalize_email(email)
      user = self.model(email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user

   # Handles superuser creation for admins (django admin page users)
   def create_superuser(self, email, password=None, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      if extra_fields.get("is_staff") is not True:
         raise ValueError("Superuser must have is_staff=True.")
      if extra_fields.get("is_superuser") is not True:
         raise ValueError("Superuser must have is_superuser=True.")

      return self.create_user(email, password, **extra_fields)

# Custom django user model
class User(AbstractBaseUser, PermissionsMixin):
   email = models.EmailField(max_length=254, unique=True, null=False)
   password = models.CharField(max_length=128)
   user_type = models.CharField(max_length=15)
   #profile_picture = models.URLField(max_length=225, null=True, blank=True)
   description = models.TextField(null=True, blank=True)
   phone_number = models.CharField(max_length=100, null=False)
   is_staff = models.BooleanField(default=True)
   is_superuser = models.BooleanField(default=False)
   is_active = models.BooleanField(default=True)

   # Links the custom django user manager to this custom user
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []
   objects = UserManager()

   # Returns user email
   def __str__(self):
      return str(self.email)

# Defines the Supporter table
class Supporter(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   name = models.CharField(max_length=100)
   denomination = models.CharField(max_length=100)
   street_address = models.CharField(max_length=100)
   city = models.CharField(max_length=100)
   state = models.CharField(max_length=100)
   country = models.CharField(max_length=100)

   # Returns supporter name, city, and state
   def __str__(self):
      return f"Supporter: {self.name}, City: {self.city}, State: {self.state}"

# Defines the Missionary table
class Missionary(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   full_name = models.CharField(max_length=100)
   denomination = models.CharField(max_length=100)
   country = models.CharField(max_length=100)
   years_of_experience = models.IntegerField()

   # Returns supporter name, city, and state
   def __str__(self):
      return f"Missionary: {self.full_name}"

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Missionaries"

# Defines the Tag table
class Tag(models.Model):
   name = models.CharField(max_length=100, null=False)
   description = models.TextField(blank=True)
   is_predefined = models.BooleanField(default=True)

# Defines the Tag Record table
class TagRecord(models.Model):
   tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   added_date = models.DateTimeField(auto_now_add=True)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Tag Records"

# Defines Search History table
class SearchHistory(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   search_time = models.DateTimeField(auto_now_add=True)
   search_text = models.TextField(null=False)
   search_parameters = models.JSONField()

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Search History"

# Defines External Media table
class ExternalMedia(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   media_url = models.URLField(max_length=255)
   description = models.TextField()
   uploaded_at = models.DateTimeField(auto_now_add=True)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "External Media"
