"""
Tests for AboutMe API views.
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.about.models import AboutMe


@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()


@pytest.fixture
def sample_about():
    """Fixture for creating a sample AboutMe profile."""
    return AboutMe.objects.create(
        name='John Doe',
        title='Software Engineer',
        bio='Experienced software engineer with expertise in Python.',
        email='john@example.com',
        phone='+1234567890',
        location='San Francisco, CA',
        linkedin_url='https://linkedin.com/in/johndoe',
        github_url='https://github.com/johndoe',
        is_active=True
    )


@pytest.fixture
def inactive_about():
    """Fixture for creating an inactive AboutMe profile."""
    return AboutMe.objects.create(
        name='Jane Smith',
        title='Data Scientist',
        bio='Data scientist specializing in ML.',
        email='jane@example.com',
        is_active=False
    )


@pytest.mark.django_db
class TestAboutMeViewSet:
    """Test suite for AboutMeViewSet."""

    def test_list_about_profiles(self, api_client, sample_about):
        """Test retrieving list of all AboutMe profiles."""
        url = '/api/about/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'John Doe'

    def test_list_about_profiles_empty(self, api_client):
        """Test retrieving empty list when no profiles exist."""
        url = '/api/about/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_list_multiple_profiles(self, api_client, sample_about, inactive_about):
        """Test retrieving list with multiple profiles."""
        url = '/api/about/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_about_profile(self, api_client, sample_about):
        """Test retrieving a single AboutMe profile by ID."""
        url = f'/api/about/{sample_about.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_about.id
        assert response.data['name'] == 'John Doe'
        assert response.data['title'] == 'Software Engineer'
        assert response.data['email'] == 'john@example.com'

    def test_retrieve_nonexistent_profile(self, api_client):
        """Test retrieving a profile that doesn't exist."""
        url = '/api/about/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_about_profile(self, api_client):
        """Test creating a new AboutMe profile."""
        url = '/api/about/'
        data = {
            'name': 'Alice Johnson',
            'title': 'Full Stack Developer',
            'bio': 'Full stack developer with 5 years of experience.',
            'email': 'alice@example.com',
            'phone': '+1987654321',
            'location': 'New York, NY',
            'linkedinUrl': 'https://linkedin.com/in/alicejohnson',
            'githubUrl': 'https://github.com/alicejohnson',
            'isActive': True
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Alice Johnson'
        assert response.data['title'] == 'Full Stack Developer'
        assert response.data['isActive'] is True
        assert AboutMe.objects.count() == 1

    def test_create_profile_missing_required_name(self, api_client):
        """Test creating a profile without required name field."""
        url = '/api/about/'
        data = {
            'title': 'Developer',
            'bio': 'Bio text',
            'email': 'test@example.com'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_create_profile_missing_required_email(self, api_client):
        """Test creating a profile without required email field."""
        url = '/api/about/'
        data = {
            'name': 'Test Name',
            'title': 'Developer',
            'bio': 'Bio text'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_create_profile_invalid_email(self, api_client):
        """Test creating a profile with invalid email."""
        url = '/api/about/'
        data = {
            'name': 'Test Name',
            'title': 'Developer',
            'bio': 'Bio text',
            'email': 'not-a-valid-email'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_update_profile_full(self, api_client, sample_about):
        """Test full update of a profile (PUT)."""
        url = f'/api/about/{sample_about.id}/'
        data = {
            'name': 'John Updated',
            'title': 'Senior Software Engineer',
            'bio': 'Updated bio with more experience.',
            'email': 'johnupdated@example.com',
            'phone': '+1111111111',
            'location': 'Los Angeles, CA',
            'linkedinUrl': 'https://linkedin.com/in/johnupdated',
            'githubUrl': 'https://github.com/johnupdated',
            'isActive': True
        }

        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'John Updated'
        assert response.data['title'] == 'Senior Software Engineer'
        assert response.data['email'] == 'johnupdated@example.com'

    def test_partial_update_profile(self, api_client, sample_about):
        """Test partial update of a profile (PATCH)."""
        url = f'/api/about/{sample_about.id}/'
        data = {
            'name': 'John Partially Updated',
            'location': 'Seattle, WA'
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'John Partially Updated'
        assert response.data['location'] == 'Seattle, WA'
        assert response.data['title'] == 'Software Engineer'  # Unchanged

    def test_delete_profile(self, api_client, sample_about):
        """Test deleting a profile."""
        profile_id = sample_about.id
        url = f'/api/about/{profile_id}/'

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not AboutMe.objects.filter(id=profile_id).exists()

    def test_active_profile_action(self, api_client, sample_about, inactive_about):
        """Test the active custom action to retrieve active profile."""
        url = '/api/about/active/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_about.id
        assert response.data['isActive'] is True
        assert response.data['name'] == 'John Doe'

    def test_active_profile_action_no_active(self, api_client, inactive_about):
        """Test active action when no profile is active."""
        url = '/api/about/active/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}

    def test_active_profile_action_empty_database(self, api_client):
        """Test active action when database is empty."""
        url = '/api/about/active/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}

    def test_create_active_profile_deactivates_others(self, api_client, sample_about):
        """Test that creating a new active profile deactivates existing ones."""
        url = '/api/about/'
        data = {
            'name': 'New Active Profile',
            'title': 'Engineer',
            'bio': 'New profile',
            'email': 'newactive@example.com',
            'isActive': True
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # Refresh the original profile
        sample_about.refresh_from_db()
        assert sample_about.is_active is False

        # Verify only one active profile
        active_count = AboutMe.objects.filter(is_active=True).count()
        assert active_count == 1

    def test_update_inactive_to_active(self, api_client, sample_about, inactive_about):
        """Test updating an inactive profile to active."""
        url = f'/api/about/{inactive_about.id}/'
        data = {'isActive': True}

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isActive'] is True

        # Check that the previously active profile is now inactive
        sample_about.refresh_from_db()
        assert sample_about.is_active is False

    def test_response_field_names_camelcase(self, api_client, sample_about):
        """Test that API responses use camelCase field names."""
        url = f'/api/about/{sample_about.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'profileImage' in response.data
        assert 'resumeFile' in response.data
        assert 'linkedinUrl' in response.data
        assert 'githubUrl' in response.data
        assert 'twitterUrl' in response.data
        assert 'websiteUrl' in response.data
        assert 'isActive' in response.data
        assert 'createdAt' in response.data
        assert 'updatedAt' in response.data

    def test_list_ordering_by_created_at_desc(self, api_client):
        """Test that profiles are ordered by created_at descending."""
        about1 = AboutMe.objects.create(
            name='First',
            title='Developer',
            bio='First profile',
            email='first@example.com'
        )
        about2 = AboutMe.objects.create(
            name='Second',
            title='Engineer',
            bio='Second profile',
            email='second@example.com'
        )

        url = '/api/about/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Most recent first
        assert response.data[0]['name'] == 'Second'
        assert response.data[1]['name'] == 'First'

    def test_api_content_type_json(self, api_client, sample_about):
        """Test that API responses have JSON content type."""
        url = f'/api/about/{sample_about.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']

    def test_create_profile_with_all_social_links(self, api_client):
        """Test creating a profile with all social media links."""
        url = '/api/about/'
        data = {
            'name': 'Social Media Person',
            'title': 'Influencer',
            'bio': 'Social media expert',
            'email': 'social@example.com',
            'linkedinUrl': 'https://linkedin.com/in/social',
            'githubUrl': 'https://github.com/social',
            'twitterUrl': 'https://twitter.com/social',
            'websiteUrl': 'https://social.com'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['linkedinUrl'] == 'https://linkedin.com/in/social'
        assert response.data['githubUrl'] == 'https://github.com/social'
        assert response.data['twitterUrl'] == 'https://twitter.com/social'
        assert response.data['websiteUrl'] == 'https://social.com'

    def test_create_profile_with_minimal_data(self, api_client):
        """Test creating a profile with only required fields."""
        url = '/api/about/'
        data = {
            'name': 'Minimal Person',
            'title': 'Developer',
            'bio': 'Minimal bio',
            'email': 'minimal@example.com'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Minimal Person'
        assert response.data['phone'] == ''
        assert response.data['location'] == ''

    def test_update_profile_social_links(self, api_client, sample_about):
        """Test updating social media links."""
        url = f'/api/about/{sample_about.id}/'
        data = {
            'twitterUrl': 'https://twitter.com/johndoe',
            'websiteUrl': 'https://johndoe.dev'
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['twitterUrl'] == 'https://twitter.com/johndoe'
        assert response.data['websiteUrl'] == 'https://johndoe.dev'

    def test_profile_not_found_returns_404(self, api_client):
        """Test that requesting non-existent profile returns 404."""
        url = '/api/about/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_only_one_profile_can_be_active(self, api_client):
        """Test that only one profile remains active when multiple are created."""
        url = '/api/about/'

        # Create first active profile
        data1 = {
            'name': 'Active 1',
            'title': 'Developer',
            'bio': 'First active',
            'email': 'active1@example.com',
            'isActive': True
        }
        api_client.post(url, data1, format='json')

        # Create second active profile
        data2 = {
            'name': 'Active 2',
            'title': 'Engineer',
            'bio': 'Second active',
            'email': 'active2@example.com',
            'isActive': True
        }
        api_client.post(url, data2, format='json')

        # Verify only one is active
        active_profiles = AboutMe.objects.filter(is_active=True)
        assert active_profiles.count() == 1
        assert active_profiles.first().name == 'Active 2'

    def test_deactivate_active_profile(self, api_client, sample_about):
        """Test deactivating the active profile."""
        url = f'/api/about/{sample_about.id}/'
        data = {'isActive': False}

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isActive'] is False

        # Verify no active profiles
        active_count = AboutMe.objects.filter(is_active=True).count()
        assert active_count == 0
