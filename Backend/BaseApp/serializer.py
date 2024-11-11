from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Supporter, Missionary,\
                    Tag, TagRecord, SearchHistory, ExternalMedia

# Serializer class for Users
class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ('id', 'email', 'user_type', 'profile_picture',
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

      user = authenticate(username=email, password=password)

      if user is None:
         raise serializers.ValidationError("A user with this email\
                                           and password was not found.")
      return user

   # Placeholders to satisfy pylint warnings about abstract requirements
   def create(self, validated_data):
      pass
   def update(self, instance, validated_data):
      pass
