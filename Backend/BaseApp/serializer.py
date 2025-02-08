from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Tag, TagRecord, SearchHistory,\
                    ExternalMedia, Profile


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
   user = UserSerializer()  # Nested User serializer

   class Meta:
      model = Profile
      fields = '__all__'

   def create(self, validated_data):
      user_data = validated_data.pop('user')
      user = User.objects.create(**user_data)
      profile = Profile.objects.create(user=user, **validated_data)
      return profile

   def update(self, instance, validated_data):
      user_data = validated_data.pop('user', None)
      if user_data:
         for key, value in user_data.items():
            setattr(instance.user, key, value)
         instance.user.save()

      for key, value in validated_data.items():
         setattr(instance, key, value)
      instance.save()
      return instance

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model =  User
      fields = '__all__'

# Serializer class for Tags
class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Tag
      fields = '__all__'

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


class RegistrationSerializer(serializers.ModelSerializer):
   # User fields
   username = serializers.CharField  (max_length=150, required=True)
   password = serializers.CharField  (max_length=128, min_length=8,
                                      write_only=True, required=True)
   first_name = serializers.CharField(max_length=100,
                                      allow_blank=True, default='')
   last_name = serializers.CharField (max_length=100,
                                      allow_blank=True, default='')
   email = serializers.EmailField    (required=True)
   # Profile fields
   user_type = serializers.ChoiceField   (choices=[('missionary', 'Missionary'),
                                                   ('supporter', 'Supporter'),
                                                   ('other', 'Other')],
                                                   required=False,
                                                   default='other')
   denomination = serializers.CharField  (max_length=100, required=False,
                                          allow_blank=True, default='')
   street_address = serializers.CharField(max_length=100, required=False,
                                          allow_blank=True, default='')
   city = serializers.CharField          (max_length=100, required=False,
                                          allow_blank=True, default='')
   state = serializers.CharField         (max_length=100, required=False,
                                          allow_blank=True, default='')
   country = serializers.CharField       (max_length=100, required=False,
                                          allow_blank=True, default='')
   phone_number = serializers.CharField  (max_length=100, required=False,
                                          allow_blank=True, default='')
   years_of_experience = serializers.IntegerField(required=False,
                                                  allow_null=True, default=None)
   description = serializers.CharField   (required=False,
                                          allow_blank=True, default=None)
   profile_picture = serializers.URLField(required=False,
                                          allow_blank=True, default=None)
   class Meta:
      model = User
      fields = ('username', 'email', 'password', 'first_name', 'last_name',
                'user_type', 'denomination', 'street_address', 'city',
                'state', 'country', 'phone_number', 'years_of_experience',
                'description', 'profile_picture')
   # Create a new user instance
   def create(self, validated_data):
      user_data = {
           'username': validated_data.pop('username'),
              'email': validated_data.pop('email'),
           'password': validated_data.pop('password'),
         'first_name': validated_data.pop('first_name', ''),
          'last_name': validated_data.pop('last_name', '')
      }
      # Create user instance
      user = User.objects.create_user(**user_data)
      # Create profile instance separately
      Profile.objects.create         (user=user, **validated_data)
      return user
