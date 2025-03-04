from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Tag, Profile

class TagTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create a test profile with all fields
        self.profile = Profile.objects.create(
            user=self.user,
            user_type='missionary',
            first_name='Test',
            last_name='User',
            denomination='Test Denomination',
            street_address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            phone_number='123-456-7890',
            years_of_experience=5,
            description='Test description'
        )
        
        # Set up the API client
        self.client = APIClient()
        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
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
        """Test creating a tag and adding it to a profile"""
        data = {
            'tag_name': 'ProfileTag',
            'tag_description': 'A tag for a profile',
            'profile_id': self.profile.user_id
        }
        response = self.client.post('/tag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(self.profile.tags.count(), 1)
        self.assertEqual(self.profile.tags.first().tag_name, 'ProfileTag')

    def test_add_tag_to_nonexistent_profile(self):
        """Test adding a tag to a profile that doesn't exist"""
        data = {
            'tag_name': 'NonexistentProfileTag',
            'tag_description': 'This should fail',
            'profile_id': 999  # Non-existent profile ID
        }
        response = self.client.post('/tag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Tag.objects.count(), 0)

    def test_add_existing_tag_to_profile(self):
        """Test adding an existing tag to a profile"""
        # First create a tag
        tag = Tag.objects.create(
            tag_name='ExistingTag',
            tag_description='An existing tag'
        )
        
        # Try to add the same tag to a profile
        data = {
            'tag_name': 'ExistingTag',
            'profile_id': self.profile.user_id
        }
        response = self.client.post('/tag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.count(), 1)  # Should not create a new tag
        self.assertEqual(self.profile.tags.count(), 1)
        self.assertEqual(self.profile.tags.first().tag_name, 'ExistingTag')

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
