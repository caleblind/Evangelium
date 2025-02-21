from rest_framework import serializers
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
   user = UserSerializer(read_only=True)  # Prevent users from modifying `user`
   tags = serializers.PrimaryKeyRelatedField(
      queryset=Tag.objects.all(), many=True, required=False
   )

   class Meta:
      model = Profile
      fields = '__all__'

   def create(self, validated_data):
      """
      Handles profile creation. The user field is automatically assigned to the request user.
      """
      request = self.context.get('request')
      if request and hasattr(request, "user"):
         validated_data["user"] = request.user  # Assign the logged-in user

      tag_data = validated_data.pop("tags", [])
      profile = Profile.objects.create(**validated_data)
      profile.tags.set(tag_data)  # Assign tags
      return profile

   def update(self, instance, validated_data):
      """
      Handles profile updates securely:
      - Users cannot modify the `user` field.
      - Regular users can update only their own profile.
      - Admins can update any profile.
      """
      request = self.context.get('request')
      
      if request and hasattr(request, "user"):
         if not request.user.is_staff and request.user != instance.user:
            raise serializers.ValidationError("You can only edit your own profile.")

      validated_data.pop("user", None)  # Prevent modification of user field

      tag_data = validated_data.pop("tags", None)
      for key, value in validated_data.items():
         setattr(instance, key, value)
      instance.save()

      if tag_data is not None:
         instance.tags.set(tag_data)  # Replace tags, not just add

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
