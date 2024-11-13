from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Supporter, Missionary,\
                    Tag, TagRecord, SearchHistory, ExternalMedia

# Serializer class for Users
class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ('id', 'email', 'password', 'user_type', #'profile_picture',
                'description', 'phone_number')

# Serializer class for Supporters
class SupporterSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Supporter
      fields = '__all__'

# Serializer class for Missionaries
class MissionarySerializer(serializers.ModelSerializer):
   class Meta:
      model  = Missionary
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

# Serializer class for user registration
class RegistrationSerializer(serializers.ModelSerializer):
   password = serializers.CharField(
      max_length=128, min_length=8, write_only=True, required=True
   )

   class Meta:
      model = User
      fields = ('email', 'password', 'user_type',
                'description', 'phone_number')

   # Handles user creation with validated data
   def create(self, validated_data):
      validated_data.pop('password_confirm', None)
      user = User.objects.create_user(
         email=validated_data['email'],
         password=validated_data['password'],
         user_type=validated_data.get('user_type', ''),
         description=validated_data.get('description', ''),
         phone_number=validated_data.get('phone_number', '')
      )
      return user
