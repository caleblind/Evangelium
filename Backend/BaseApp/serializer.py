from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Tag, TagRecord, SearchHistory,\
                    ExternalMedia, Profile

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

# Serializer for profile model
class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Profile
      fields = ('user_type','first_name','last_name',
                'denomination','street_address','city',
                'state','country','phone_number', 
                'years_of_experience','description','profile_picture')

# Dynamically fetch Django's User model and store in global variable
User = get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
   password = serializers.CharField(max_length=128, min_length=8,
                                    write_only=True, required=True)
   profile = ProfileSerializer(required=True)

   class Meta:
      model = User
      fields = ('email', 'password', 'first_name', 'last_name')

   # Create a new user instance
   def create(self, validated_data):
      # Extract the profile data separately
      profile_data = validated_data.pop('profile')

      user = User.objects.create_user(
         email      = validated_data['email'],
         password   = validated_data['password'],
         first_name = validated_data.get('first_name', ''),
         last_name  = validated_data.get('last_name', '')
      )
      # Create profile instance separately
      profile = Profile.objects.create(**profile_data)
      return {'user': user,
              'profile': profile}
