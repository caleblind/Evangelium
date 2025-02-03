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


# Dynamically fetch Django's User model and store in global variable
User = get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
   # User fields
   username = serializers.CharField(max_length=150, required=True)
   password = serializers.CharField(max_length=128, min_length=8,
                                    write_only=True, required=True)
   first_name = serializers.CharField(max_length=100, required=True)
   last_name = serializers.CharField(max_length=100, required=True)
   email = serializers.EmailField(required=True)

   # Profile fields (flattened)
   user_type = serializers.ChoiceField(choices=[('missionary', 'Missionary'),
                                                 ('supporter', 'Supporter'),
                                                 ('other', 'Other')],
                                                 default='other')
   denomination = serializers.CharField(max_length=100, required=True)
   street_address = serializers.CharField(max_length=100, required=True)
   city = serializers.CharField(max_length=100, required=True)
   state = serializers.CharField(max_length=100, required=True)
   country = serializers.CharField(max_length=100, required=True)
   phone_number = serializers.CharField(max_length=100, required=True)
   years_of_experience = serializers.IntegerField(required=False,
                                                  allow_null=True)
   description = serializers.CharField(required=False, allow_blank=True,
                                       allow_null=True)
   profile_picture = serializers.URLField(required=False,
                                          allow_blank=True, allow_null=True)

   class Meta:
      model = User
      fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'user_type', 'denomination', 'street_address', 'city',
                  'state', 'country', 'phone_number', 'years_of_experience',
                  'description', 'profile_picture')
   # Create a new user instance
   def create(self, validated_data):
      user_data = {
         'username':   validated_data.pop('username'),
         'email':      validated_data.pop('email'),
         'password':   validated_data.pop('password'),
         'first_name': validated_data.pop('first_name'),
         'last_name':  validated_data.pop('last_name')
      }
      # Create user instance
      user = User.objects.create_user(**user_data)
      # Create profile instance separately
      Profile.objects.create(user=user, **validated_data)
      return user
