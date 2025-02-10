from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'password']

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
         for key, value in user_data.items():
            setattr(instance.user, key, value)
         instance.user.save()

      for key, value in validated_data.items():
         setattr(instance, key, value)
      instance.save()

      if tag_data is not None:
         instance.tags.add(tag_data)  # Add the new tags to the profile
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

# Serializer class for user login
class LoginSerializer(serializers.Serializer):
   email = serializers.EmailField(max_length=255)
   password = serializers.CharField(max_length=128)

   # Validates user login
   def validate(self, attrs):
      email = attrs.get("email", None)
      password = attrs.get("password", None)
      if email is None:
         raise serializers.ValidationError("An email is required to log in.")
      if password is None:
         raise serializers.ValidationError("A password is required to log in.")
      user = authenticate(email=email, password=password)
      if user is None:
         raise serializers.ValidationError(
            "A user with this email and password was not found."
         )
      return user

   # Placeholders to satisfy pylint warnings about abstract requirements
   def create(self, validated_data):
      pass
   def update(self, instance, validated_data):
      pass
