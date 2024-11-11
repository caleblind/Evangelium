from rest_framework import serializers
#from django.contrib.auth import authenticate
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
#class LoginSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   password = serializers.CharField(max_length=128)

   # Authenticates user with proided email and password
#   def validate(self, data):
