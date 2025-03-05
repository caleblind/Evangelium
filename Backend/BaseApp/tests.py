from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Tag, Profile, ProfileTagging
from django.db import transaction

class TagTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Create test profiles
        self.profile1 = Profile.objects.create(
            user=self.user1,
            user_type='missionary',
            first_name='Test',
            last_name='User1',
            denomination='Test Denomination',
            street_address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            phone_number='123-456-7890',
            years_of_experience=5,
            description='Test description'
        )
        
        self.profile2 = Profile.objects.create(
            user=self.user2,
            user_type='supporter',
            first_name='Test',
            last_name='User2',
            denomination='Test Denomination',
            street_address='456 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            phone_number='987-654-3210',
            years_of_experience=3,
            description='Test description'
        )
        
        # Set up the API client for user1
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_tag(self):
        """Test creating a new tag without adding it to a profile"""
        data = {
            'tag_name': 'TestTag',
            'tag_description': 'A test tag',
            'tag_is_predefined': False
        }
        response = self.client.post('/tag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().tag_name, 'TestTag')

    def test_add_tag_to_profile(self):
        """Test adding a tag to a profile"""
        data = {
            'tag_name': 'ProfileTag',
            'tag_description': 'A tag for a profile',
            'profile_id': self.profile1.user_id
        }
        response = self.client.post('/api/tag/add-to-profile/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(self.profile1.tags.count(), 1)
        
        # Verify the tag was added with correct metadata
        tagging = ProfileTagging.objects.first()
        self.assertEqual(tagging.added_by, self.user1)
        self.assertEqual(tagging.profile, self.profile1)
        self.assertEqual(tagging.tag.tag_name, 'ProfileTag')

    def test_add_tag_to_other_profile(self):
        """Test adding a tag to another user's profile"""
        data = {
            'tag_name': 'OtherUserTag',
            'tag_description': 'A tag for another user',
            'profile_id': self.profile2.user_id
        }
        response = self.client.post('/api/tag/add-to-profile/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(self.profile2.tags.count(), 1)
        
        # Verify the tag was added with correct metadata
        tagging = ProfileTagging.objects.first()
        self.assertEqual(tagging.added_by, self.user1)
        self.assertEqual(tagging.profile, self.profile2)
        self.assertEqual(tagging.tag.tag_name, 'OtherUserTag')

    def test_tags_added_to_others_property(self):
        """Test the tags_added_to_others property"""
        # Add a tag to user2's profile
        tag = Tag.objects.create(
            tag_name='TestTag',
            tag_description='Test description'
        )
        ProfileTagging.objects.create(
            profile=self.profile2,
            tag=tag,
            added_by=self.user1
        )
        
        # Verify the property returns the correct tag
        self.assertEqual(list(self.profile1.tags_added_to_others), [tag])

    def test_cannot_add_duplicate_tag(self):
        """Test that a user cannot add the same tag to the same profile twice"""
        with transaction.atomic():
            # First add a tag
            data = {
                'tag_name': 'DuplicateTag',
                'tag_description': 'This should fail on second attempt',
                'profile_id': self.profile2.user_id
            }
            response = self.client.post('/api/tag/add-to-profile/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Try to add the same tag again
            response = self.client.post('/api/tag/add-to-profile/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(ProfileTagging.objects.count(), 1)

    def test_add_tag_to_nonexistent_profile(self):
        """Test adding a tag to a profile that doesn't exist"""
        data = {
            'tag_name': 'NonexistentProfileTag',
            'tag_description': 'This should fail',
            'profile_id': 999  # Non-existent profile ID
        }
        response = self.client.post('/api/tag/add-to-profile/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Tag.objects.count(), 0)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot create tags"""
        # Remove authentication credentials
        self.client.credentials()
        
        data = {
            'tag_name': 'UnauthenticatedTag',
            'tag_description': 'This should fail'
        }
        response = self.client.post('/tag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Tag.objects.count(), 0)
