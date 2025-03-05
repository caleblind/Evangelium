from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Defines the Tag table
class Tag(models.Model):
   tag_name = models.CharField(max_length=100, null=False)
   tag_description = models.TextField(blank=True)
   tag_is_predefined = models.BooleanField(default=True)

   def __str__(self):
      return str(self.tag_name)

# Through model for user-added tags
class ProfileTagging(models.Model):
   profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile_taggings')
   tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
   added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tags_added')
   added_at = models.DateTimeField(auto_now_add=True)

   class Meta:
      unique_together = ['profile', 'tag', 'added_by']
      verbose_name = "Profile Tagging"
      verbose_name_plural = "Profile Taggings"

# Defines the Profile table
class Profile(models.Model):
   user = models.OneToOneField(
      User,
      on_delete=models.CASCADE, primary_key=True)
   user_type = models.CharField(
        max_length=15,
        choices=[('missionary', 'Missionary'), ('supporter', 'Supporter'),
                 ('other', 'Other')],
        default='other',  blank=True, null=True
    )
   first_name = models.CharField(max_length=100, blank=True, null=True)
   last_name = models.CharField(max_length=100, blank=True, null=True)
   denomination = models.CharField(max_length=100, blank=True, null=True)
   street_address = models.CharField(max_length=100, blank=True, null=True)
   city = models.CharField(max_length=100, blank=True, null=True)
   state = models.CharField(max_length=100, blank=True, null=True)
   country = models.CharField(max_length=100, blank=True, null=True)
   phone_number = models.CharField(max_length=100, blank=True, null=True)
   years_of_experience = models.IntegerField(blank=True, null=True)
   description = models.TextField(blank=True, null=True)
   profile_picture = models.URLField(max_length=225, null=True, blank=True)

   # Tags with additional metadata through the intermediate model
   tags = models.ManyToManyField(Tag, through='ProfileTagging', related_name='profiles', blank=True)

   def __str__(self):
      return f"{self.user.username} - {self.user_type}" # pylint: disable=no-member

   @property
   def tags_added_to_others(self):
      """Get tags that this user added to other profiles"""
      return Tag.objects.filter(
         profiletagging__added_by=self.user
      ).exclude(
         profiletagging__profile__user=self.user
      ).distinct()

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
