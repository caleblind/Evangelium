from rest_framework import serializers
from .models import Profile, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']

class ProfileSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user_type', 'first_name', 'last_name', 'description',
            'profile_picture', 'denomination', 'city', 'state', 'country',
            'tags'
        ] 