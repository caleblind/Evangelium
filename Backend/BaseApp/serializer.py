from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Tag, TagRecord, SearchHistory,\
                    ExternalMedia, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer class for Tags
class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Tag
      fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tags = TagSerializer(many=True)  # ✅ Nested serialization for full CRUD

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        tags_data = validated_data.pop('tags', [])  # ✅ Extract tags safely

        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)

        # ✅ Create new tags if they don’t exist & assign them
        tag_instances = []
        for tag_data in tags_data:
            tag_instance, _ = Tag.objects.get_or_create(name=tag_data['name'])
            tag_instances.append(tag_instance)

        profile.tags.set(tag_instances)  # ✅ Assign Many-to-Many tags properly
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        tags_data = validated_data.pop('tags', None)

        if user_data:
            for key, value in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if tags_data is not None:
            tag_instances = []
            for tag_data in tags_data:
                tag_instance, _ = Tag.objects.get_or_create(name=tag_data['name'])
                tag_instances.append(tag_instance)

            instance.tags.set(tag_instances)  # ✅ Replace old tags with new ones

        return instance



# Serializer class for Tag Records
class TagRecordSerializer(serializers.ModelSerializer):
   class Meta:
      model  = TagRecord
      fields = '__all__'

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
