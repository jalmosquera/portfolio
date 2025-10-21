"""
Tests for Project serializers.
"""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.projects.models import Project
from apps.projects.api.serializers import ProjectSerializer


@pytest.mark.django_db
class TestProjectSerializer:
    """Test suite for ProjectSerializer."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid data."""
        data = {
            'title': 'New Project',
            'description': 'Project description',
            'shortDescription': 'Short desc',
            'url': 'https://example.com',
            'githubUrl': 'https://github.com/user/repo',
            'technologies': 'Python, Django',
            'isFeatured': True,
            'order': 1
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert project.title == 'New Project'
        assert project.description == 'Project description'
        assert project.short_description == 'Short desc'
        assert project.url == 'https://example.com'
        assert project.github_url == 'https://github.com/user/repo'
        assert project.technologies == 'Python, Django'
        assert project.is_featured is True
        assert project.order == 1

    def test_serializer_with_minimal_data(self):
        """Test serializer with only required fields."""
        data = {
            'title': 'Minimal Project',
            'description': 'Minimal description'
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert project.title == 'Minimal Project'
        assert project.description == 'Minimal description'
        assert project.short_description == ''
        assert project.is_featured is False

    def test_serializer_missing_required_title(self):
        """Test serializer validation fails when title is missing."""
        data = {
            'description': 'Description without title'
        }

        serializer = ProjectSerializer(data=data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors

    def test_serializer_missing_required_description(self):
        """Test serializer validation fails when description is missing."""
        data = {
            'title': 'Title without description'
        }

        serializer = ProjectSerializer(data=data)
        assert not serializer.is_valid()
        assert 'description' in serializer.errors

    def test_serializer_camelcase_field_mapping(self):
        """Test that camelCase fields map correctly to snake_case."""
        project = Project.objects.create(
            title='Camel Case Test',
            description='Testing field mapping',
            short_description='Brief summary',
            github_url='https://github.com/test',
            is_featured=True
        )

        serializer = ProjectSerializer(project)

        assert 'shortDescription' in serializer.data
        assert 'githubUrl' in serializer.data
        assert 'isFeatured' in serializer.data
        assert 'createdAt' in serializer.data
        assert 'updatedAt' in serializer.data

        assert serializer.data['shortDescription'] == 'Brief summary'
        assert serializer.data['githubUrl'] == 'https://github.com/test'
        assert serializer.data['isFeatured'] is True

    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be modified via serializer."""
        project = Project.objects.create(
            title='Read-only Test',
            description='Testing read-only fields'
        )

        original_id = project.id
        original_created = project.created_at

        data = {
            'id': 99999,
            'title': 'Updated Title',
            'description': 'Updated description',
            'createdAt': '2020-01-01T00:00:00Z',
            'updatedAt': '2020-01-01T00:00:00Z'
        }

        serializer = ProjectSerializer(project, data=data)
        assert serializer.is_valid()
        updated_project = serializer.save()

        # ID and createdAt should not change
        assert updated_project.id == original_id
        assert updated_project.created_at == original_created
        # Title and description should update
        assert updated_project.title == 'Updated Title'
        assert updated_project.description == 'Updated description'

    def test_serializer_url_validation(self):
        """Test that URL fields are validated."""
        data = {
            'title': 'URL Test',
            'description': 'Testing URL validation',
            'url': 'not-a-valid-url'
        }

        serializer = ProjectSerializer(data=data)
        assert not serializer.is_valid()
        assert 'url' in serializer.errors

    def test_serializer_github_url_validation(self):
        """Test that GitHub URL field is validated."""
        data = {
            'title': 'GitHub URL Test',
            'description': 'Testing GitHub URL validation',
            'githubUrl': 'invalid-github-url'
        }

        serializer = ProjectSerializer(data=data)
        assert not serializer.is_valid()
        assert 'githubUrl' in serializer.errors

    def test_serializer_blank_optional_fields(self):
        """Test that optional fields can be blank."""
        data = {
            'title': 'Optional Fields Test',
            'description': 'Testing optional fields',
            'shortDescription': '',
            'url': '',
            'githubUrl': '',
            'technologies': ''
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_boolean_field_default(self):
        """Test that isFeatured has correct default value."""
        data = {
            'title': 'Boolean Default Test',
            'description': 'Testing boolean default'
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert project.is_featured is False

    def test_serializer_output_structure(self):
        """Test that serializer output has all expected fields."""
        project = Project.objects.create(
            title='Structure Test',
            description='Testing output structure'
        )

        serializer = ProjectSerializer(project)
        expected_fields = {
            'id', 'title', 'description', 'shortDescription',
            'imageUrl', 'url', 'githubUrl', 'technologies',
            'isFeatured', 'order', 'createdAt', 'updatedAt'
        }

        assert set(serializer.data.keys()) == expected_fields

    def test_serializer_update_partial(self):
        """Test partial update of a project."""
        project = Project.objects.create(
            title='Original Title',
            description='Original description',
            order=1
        )

        data = {'title': 'Updated Title'}

        serializer = ProjectSerializer(project, data=data, partial=True)
        assert serializer.is_valid()
        updated_project = serializer.save()

        assert updated_project.title == 'Updated Title'
        assert updated_project.description == 'Original description'
        assert updated_project.order == 1

    def test_serializer_with_image_field(self):
        """Test serializer with image file."""
        # Create a simple image file
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

        data = {
            'title': 'Image Test',
            'description': 'Testing image field',
            'imageUrl': image_file
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert project.image.name != ''
        assert 'test_image' in project.image.name

    def test_serializer_technologies_as_string(self):
        """Test that technologies field is stored as string."""
        data = {
            'title': 'Tech String Test',
            'description': 'Testing technologies as string',
            'technologies': 'Python, Django, React, PostgreSQL'
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert isinstance(project.technologies, str)
        assert project.technologies == 'Python, Django, React, PostgreSQL'

    def test_serializer_order_field_integer(self):
        """Test that order field accepts integers."""
        data = {
            'title': 'Order Test',
            'description': 'Testing order field',
            'order': 42
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert project.order == 42

    def test_serializer_order_field_negative(self):
        """Test that order field can be negative."""
        data = {
            'title': 'Negative Order Test',
            'description': 'Testing negative order',
            'order': -5
        }

        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid()
        project = serializer.save()

        assert project.order == -5

    def test_serializer_list_serialization(self):
        """Test serializing multiple projects."""
        Project.objects.create(
            title='Project 1',
            description='First project'
        )
        Project.objects.create(
            title='Project 2',
            description='Second project'
        )

        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)

        assert len(serializer.data) == 2
        assert serializer.data[0]['title'] in ['Project 1', 'Project 2']
        assert serializer.data[1]['title'] in ['Project 1', 'Project 2']

    def test_serializer_null_image_field(self):
        """Test that imageUrl can be null."""
        project = Project.objects.create(
            title='Null Image Test',
            description='Testing null image'
        )

        serializer = ProjectSerializer(project)

        assert serializer.data['imageUrl'] is None

    def test_serializer_featured_toggle(self):
        """Test toggling isFeatured field."""
        project = Project.objects.create(
            title='Featured Toggle',
            description='Testing featured toggle',
            is_featured=False
        )

        data = {'isFeatured': True}
        serializer = ProjectSerializer(project, data=data, partial=True)
        assert serializer.is_valid()
        updated_project = serializer.save()

        assert updated_project.is_featured is True
