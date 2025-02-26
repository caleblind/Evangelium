from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'password']
      extra_kwargs = {
         'username': {'read_only': True},
         'email': {'read_only': True},
         'password': {'write_only': True}
      }

# Serializer class for Tags
class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Tag
      fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
   user = UserSerializer()  # Nested User serializer
   tags = serializers.PrimaryKeyRelatedField(
       queryset=Tag.objects.all(), many=True, required=False)

   class Meta:
      model = Profile
      fields = '__all__'

   def create(self, validated_data):
      user_data = validated_data.pop('user')
      tag_data = validated_data.pop('tags', [])
      user = User.objects.create_user(**user_data)
      profile = Profile.objects.create(user=user, **validated_data)
      profile.tags.set(tag_data)
      return profile


   def update(self, instance, validated_data):
      user_data = validated_data.pop('user', None)
      tag_data = validated_data.pop('tags', None)
      if user_data:
         user_instance = instance.user
         for key, value in user_data.items():
            setattr(instance.user, key, value)
         user_instance.save()

      for key, value in validated_data.items():
         setattr(instance, key, value)
      instance.save()

      if tag_data is not None:
         instance.tags.set(tag_data)  # Add the new tags to the profile
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
