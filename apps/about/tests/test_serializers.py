"""
Tests for AboutMe serializers.
"""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.about.models import AboutMe
from apps.about.api.serializers import AboutMeSerializer


@pytest.mark.django_db
class TestAboutMeSerializer:
    """Test suite for AboutMeSerializer."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid data."""
        data = {
            'name': 'John Doe',
            'title': 'Software Engineer',
            'bio': 'Experienced software engineer with expertise in Python and Django.',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'location': 'San Francisco, CA',
            'linkedinUrl': 'https://linkedin.com/in/johndoe',
            'githubUrl': 'https://github.com/johndoe',
            'twitterUrl': 'https://twitter.com/johndoe',
            'websiteUrl': 'https://johndoe.dev',
            'isActive': True
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.name == 'John Doe'
        assert about.title == 'Software Engineer'
        assert about.bio == 'Experienced software engineer with expertise in Python and Django.'
        assert about.email == 'john@example.com'
        assert about.phone == '+1234567890'
        assert about.location == 'San Francisco, CA'
        assert about.linkedin_url == 'https://linkedin.com/in/johndoe'
        assert about.github_url == 'https://github.com/johndoe'
        assert about.twitter_url == 'https://twitter.com/johndoe'
        assert about.website_url == 'https://johndoe.dev'
        assert about.is_active is True

    def test_serializer_with_minimal_data(self):
        """Test serializer with only required fields."""
        data = {
            'name': 'Jane Smith',
            'title': 'Developer',
            'bio': 'Developer bio',
            'email': 'jane@example.com'
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.name == 'Jane Smith'
        assert about.title == 'Developer'
        assert about.bio == 'Developer bio'
        assert about.email == 'jane@example.com'
        assert about.phone == ''
        assert about.location == ''
        assert about.is_active is True

    def test_serializer_missing_required_name(self):
        """Test serializer validation fails when name is missing."""
        data = {
            'title': 'Developer',
            'bio': 'Bio text',
            'email': 'test@example.com'
        }

        serializer = AboutMeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_serializer_missing_required_title(self):
        """Test serializer validation fails when title is missing."""
        data = {
            'name': 'Test Name',
            'bio': 'Bio text',
            'email': 'test@example.com'
        }

        serializer = AboutMeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors

    def test_serializer_missing_required_bio(self):
        """Test serializer validation fails when bio is missing."""
        data = {
            'name': 'Test Name',
            'title': 'Developer',
            'email': 'test@example.com'
        }

        serializer = AboutMeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'bio' in serializer.errors

    def test_serializer_missing_required_email(self):
        """Test serializer validation fails when email is missing."""
        data = {
            'name': 'Test Name',
            'title': 'Developer',
            'bio': 'Bio text'
        }

        serializer = AboutMeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_serializer_camelcase_field_mapping(self):
        """Test that camelCase fields map correctly to snake_case."""
        about = AboutMe.objects.create(
            name='Camel Case Test',
            title='Developer',
            bio='Testing field mapping',
            email='camel@example.com',
            linkedin_url='https://linkedin.com/test',
            github_url='https://github.com/test',
            twitter_url='https://twitter.com/test',
            website_url='https://test.dev',
            is_active=True
        )

        serializer = AboutMeSerializer(about)

        assert 'profileImage' in serializer.data
        assert 'resumeFile' in serializer.data
        assert 'linkedinUrl' in serializer.data
        assert 'githubUrl' in serializer.data
        assert 'twitterUrl' in serializer.data
        assert 'websiteUrl' in serializer.data
        assert 'isActive' in serializer.data
        assert 'createdAt' in serializer.data
        assert 'updatedAt' in serializer.data

        assert serializer.data['linkedinUrl'] == 'https://linkedin.com/test'
        assert serializer.data['githubUrl'] == 'https://github.com/test'
        assert serializer.data['twitterUrl'] == 'https://twitter.com/test'
        assert serializer.data['websiteUrl'] == 'https://test.dev'
        assert serializer.data['isActive'] is True

    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be modified via serializer."""
        about = AboutMe.objects.create(
            name='Read-only Test',
            title='Developer',
            bio='Testing read-only fields',
            email='readonly@example.com'
        )

        original_id = about.id
        original_created = about.created_at

        data = {
            'id': 99999,
            'name': 'Updated Name',
            'title': 'Updated Title',
            'bio': 'Updated bio',
            'email': 'updated@example.com',
            'createdAt': '2020-01-01T00:00:00Z',
            'updatedAt': '2020-01-01T00:00:00Z'
        }

        serializer = AboutMeSerializer(about, data=data)
        assert serializer.is_valid()
        updated_about = serializer.save()

        # ID and createdAt should not change
        assert updated_about.id == original_id
        assert updated_about.created_at == original_created
        # Other fields should update
        assert updated_about.name == 'Updated Name'
        assert updated_about.email == 'updated@example.com'

    def test_serializer_email_validation(self):
        """Test that email field is validated."""
        data = {
            'name': 'Email Test',
            'title': 'Developer',
            'bio': 'Testing email validation',
            'email': 'not-a-valid-email'
        }

        serializer = AboutMeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_serializer_url_validation(self):
        """Test that URL fields are validated."""
        data = {
            'name': 'URL Test',
            'title': 'Developer',
            'bio': 'Testing URL validation',
            'email': 'test@example.com',
            'linkedinUrl': 'not-a-valid-url'
        }

        serializer = AboutMeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'linkedinUrl' in serializer.errors

    def test_serializer_blank_optional_fields(self):
        """Test that optional fields can be blank."""
        data = {
            'name': 'Optional Test',
            'title': 'Developer',
            'bio': 'Testing optional fields',
            'email': 'optional@example.com',
            'phone': '',
            'location': '',
            'linkedinUrl': '',
            'githubUrl': '',
            'twitterUrl': '',
            'websiteUrl': ''
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_boolean_field_default(self):
        """Test that isActive has correct default value."""
        data = {
            'name': 'Boolean Test',
            'title': 'Developer',
            'bio': 'Testing boolean default',
            'email': 'boolean@example.com'
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.is_active is True

    def test_serializer_output_structure(self):
        """Test that serializer output has all expected fields."""
        about = AboutMe.objects.create(
            name='Structure Test',
            title='Developer',
            bio='Testing output structure',
            email='structure@example.com'
        )

        serializer = AboutMeSerializer(about)
        expected_fields = {
            'id', 'name', 'title', 'bio', 'email', 'phone', 'location',
            'profileImage', 'resumeFile', 'linkedinUrl', 'githubUrl',
            'twitterUrl', 'websiteUrl', 'isActive', 'createdAt', 'updatedAt'
        }

        assert set(serializer.data.keys()) == expected_fields

    def test_serializer_update_partial(self):
        """Test partial update of an AboutMe profile."""
        about = AboutMe.objects.create(
            name='Original Name',
            title='Original Title',
            bio='Original bio',
            email='original@example.com',
            location='New York'
        )

        data = {'name': 'Updated Name', 'location': 'San Francisco'}

        serializer = AboutMeSerializer(about, data=data, partial=True)
        assert serializer.is_valid()
        updated_about = serializer.save()

        assert updated_about.name == 'Updated Name'
        assert updated_about.location == 'San Francisco'
        assert updated_about.title == 'Original Title'
        assert updated_about.bio == 'Original bio'

    def test_serializer_with_profile_image(self):
        """Test serializer with profile image file."""
        image_file = SimpleUploadedFile(
            name='profile.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

        data = {
            'name': 'Image Test',
            'title': 'Developer',
            'bio': 'Testing image field',
            'email': 'image@example.com',
            'profileImage': image_file
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.profile_image.name != ''
        assert 'profile' in about.profile_image.name

    def test_serializer_with_resume_file(self):
        """Test serializer with resume file."""
        resume_file = SimpleUploadedFile(
            name='resume.pdf',
            content=b'fake pdf content',
            content_type='application/pdf'
        )

        data = {
            'name': 'Resume Test',
            'title': 'Developer',
            'bio': 'Testing resume field',
            'email': 'resume@example.com',
            'resumeFile': resume_file
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.resume_file.name != ''
        assert 'resume' in about.resume_file.name

    def test_serializer_null_image_field(self):
        """Test that profileImage can be null."""
        about = AboutMe.objects.create(
            name='Null Image Test',
            title='Developer',
            bio='Testing null image',
            email='nullimage@example.com'
        )

        serializer = AboutMeSerializer(about)

        assert serializer.data['profileImage'] is None

    def test_serializer_null_resume_field(self):
        """Test that resumeFile can be null."""
        about = AboutMe.objects.create(
            name='Null Resume Test',
            title='Developer',
            bio='Testing null resume',
            email='nullresume@example.com'
        )

        serializer = AboutMeSerializer(about)

        assert serializer.data['resumeFile'] is None

    def test_serializer_toggle_active_status(self):
        """Test toggling isActive field."""
        about = AboutMe.objects.create(
            name='Active Toggle',
            title='Developer',
            bio='Testing active toggle',
            email='toggle@example.com',
            is_active=True
        )

        data = {'isActive': False}
        serializer = AboutMeSerializer(about, data=data, partial=True)
        assert serializer.is_valid()
        updated_about = serializer.save()

        assert updated_about.is_active is False

    def test_serializer_list_serialization(self):
        """Test serializing multiple AboutMe profiles."""
        AboutMe.objects.create(
            name='Profile 1',
            title='Developer',
            bio='First profile',
            email='profile1@example.com'
        )
        AboutMe.objects.create(
            name='Profile 2',
            title='Engineer',
            bio='Second profile',
            email='profile2@example.com'
        )

        profiles = AboutMe.objects.all()
        serializer = AboutMeSerializer(profiles, many=True)

        assert len(serializer.data) == 2
        assert serializer.data[0]['name'] in ['Profile 1', 'Profile 2']
        assert serializer.data[1]['name'] in ['Profile 1', 'Profile 2']

    def test_serializer_all_social_urls(self):
        """Test serializer with all social media URLs."""
        data = {
            'name': 'Social Test',
            'title': 'Developer',
            'bio': 'Testing all social URLs',
            'email': 'social@example.com',
            'linkedinUrl': 'https://linkedin.com/in/test',
            'githubUrl': 'https://github.com/test',
            'twitterUrl': 'https://twitter.com/test',
            'websiteUrl': 'https://test.com'
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.linkedin_url == 'https://linkedin.com/in/test'
        assert about.github_url == 'https://github.com/test'
        assert about.twitter_url == 'https://twitter.com/test'
        assert about.website_url == 'https://test.com'

    def test_serializer_phone_format(self):
        """Test that phone field accepts various formats."""
        data = {
            'name': 'Phone Test',
            'title': 'Developer',
            'bio': 'Testing phone format',
            'email': 'phone@example.com',
            'phone': '+1 (555) 123-4567'
        }

        serializer = AboutMeSerializer(data=data)
        assert serializer.is_valid()
        about = serializer.save()

        assert about.phone == '+1 (555) 123-4567'
