from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile, ProfileTagging

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'password']
      extra_kwargs = {
         'password': {'write_only': True},
         'id': {'read_only': True}
      }

   def create(self, validated_data):
      return User.objects.create_user(**validated_data)

# Serializer class for Tags
class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Tag
      fields = '__all__'

class ProfileTaggingSerializer(serializers.ModelSerializer):
   tag = TagSerializer()
   
   class Meta:
      model = ProfileTagging
      fields = ['tag', 'is_self_added', 'added_by', 'added_at']

class ProfileSerializer(serializers.ModelSerializer):
   user = UserSerializer()
   taggings = ProfileTaggingSerializer(source='profiletagging_set', many=True, read_only=True)
   self_tags = serializers.SerializerMethodField()
   other_tags = serializers.SerializerMethodField()

   class Meta:
      model = Profile
      fields = ['user', 'user_type', 'first_name', 'last_name', 'denomination',
               'street_address', 'city', 'state', 'country', 'phone_number',
               'years_of_experience', 'description', 'profile_picture',
               'taggings', 'self_tags', 'other_tags']

   def get_self_tags(self, obj):
      return TagSerializer(
         Tag.objects.filter(
            profiletagging__profile=obj,
            profiletagging__is_self_added=True
         ),
         many=True
      ).data

   def get_other_tags(self, obj):
      return TagSerializer(
         Tag.objects.filter(
            profiletagging__profile=obj,
            profiletagging__is_self_added=False
         ),
         many=True
      ).data

   def create(self, validated_data):
      user_data = validated_data.pop('user')
      user = User.objects.create_user(**user_data)
      profile = Profile.objects.create(user=user, **validated_data)
      return profile

   def update(self, instance, validated_data):
      user_data = validated_data.pop('user', None)
      if user_data:
         user_instance = instance.user
         for key, value in user_data.items():
            if key != 'password':  # Don't update password through this method
               setattr(user_instance, key, value)
         user_instance.save()

      # Update all profile fields
      for key, value in validated_data.items():
         if hasattr(instance, key):  # Only set if the field exists
            setattr(instance, key, value)
      instance.save()
      return instance

# Serializer class for Search History
class SeachHistorySerializer(serializers.ModelSerializer):
   class Meta:
      model  = SearchHistory
      fields = '__all__'

# Serializer class for External Media
class ExternalMediaSerializer(serializers.ModelSerializer):
   class Meta:
      model  = ExternalMedia
      fields = '__all__'
