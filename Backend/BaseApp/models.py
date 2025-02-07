from django.db import models
from django.conf import settings

# Defines the Tag table
class Tag(models.Model):
   tag_name = models.CharField(max_length=100, null=False)
   tag_description = models.TextField(blank=True)
   tag_is_predefined = models.BooleanField(default=True)

# Defines the Supporter table
class Profile(models.Model):
   user = models.OneToOneField(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, primary_key=True)
   user_type = models.CharField(
        max_length=15,
        choices=[('missionary', 'Missionary'), ('supporter', 'Supporter'),
                 ('other', 'Other')],
        default='other'
    )
   first_name = models.CharField(max_length=100)
   last_name = models.CharField(max_length=100)
   denomination = models.CharField(max_length=100)
   street_address = models.CharField(max_length=100)
   city = models.CharField(max_length=100)
   state = models.CharField(max_length=100)
   country = models.CharField(max_length=100)
   phone_number = models.CharField(max_length=100)
   years_of_experience = models.IntegerField(blank=True, null=True)
   description = models.TextField(blank=True, null=True)
   profile_picture = models.URLField(max_length=225, null=True, blank=True)

   #tags = models.ManyToManyField(Tag, blank=True)



# Defines the Tag Record table
class TagRecord(models.Model):
   tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   added_date = models.DateTimeField(auto_now_add=True)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Tag Records"

# Defines Search History table
class SearchHistory(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   search_time = models.DateTimeField(auto_now_add=True)
   search_text = models.TextField(null=False)
   search_parameters = models.JSONField()

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Search History"

# Defines External Media table
class ExternalMedia(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   media_url = models.URLField(max_length=255)
   description = models.TextField()
   uploaded_at = models.DateTimeField(auto_now_add=True)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "External Media"
