from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile

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


class ProfileSerializer(serializers.ModelSerializer):
   user = UserSerializer()  # Nested User serializer
   tags = TagSerializer(many=True)  # Use TagSerializer for tags

   class Meta:
      model = Profile
      fields = '__all__'

   def create(self, validated_data):
      user_data = validated_data.pop('user')
      tags_data = validated_data.pop('tags', [])
      user = User.objects.create_user(**user_data)
      profile = Profile.objects.create(user=user, **validated_data)
      
      # Handle tags
      for tag_data in tags_data:
         tag, _ = Tag.objects.get_or_create(tag_name=tag_data['tag_name'])
         profile.tags.add(tag)
      
      return profile

   def update(self, instance, validated_data):
      user_data = validated_data.pop('user', None)
      tags_data = validated_data.pop('tags', None)

      # Update user fields if provided
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

      # Update tags if provided
      if tags_data is not None:
         instance.tags.clear()  # Remove all existing tags
         for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(tag_name=tag_data['tag_name'])
            instance.tags.add(tag)

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
