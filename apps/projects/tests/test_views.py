"""
Tests for Project API views.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.projects.models import Project


@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()


@pytest.fixture
def sample_project():
    """Fixture for creating a sample project."""
    return Project.objects.create(
        title='Sample Project',
        description='Sample description',
        short_description='Brief summary',
        url='https://example.com',
        github_url='https://github.com/user/repo',
        technologies='Python, Django',
        is_featured=False,
        order=1
    )


@pytest.fixture
def featured_project():
    """Fixture for creating a featured project."""
    return Project.objects.create(
        title='Featured Project',
        description='Featured project description',
        is_featured=True,
        order=0
    )


@pytest.mark.django_db
class TestProjectViewSet:
    """Test suite for ProjectViewSet."""

    def test_list_projects(self, api_client):
        """Test retrieving list of all projects."""
        Project.objects.create(title='Project 1', description='Description 1')
        Project.objects.create(title='Project 2', description='Description 2')

        url = '/api/projects/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_list_projects_empty(self, api_client):
        """Test retrieving empty list when no projects exist."""
        url = '/api/projects/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_retrieve_project(self, api_client, sample_project):
        """Test retrieving a single project by ID."""
        url = f'/api/projects/{sample_project.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_project.id
        assert response.data['title'] == 'Sample Project'
        assert response.data['description'] == 'Sample description'

    def test_retrieve_nonexistent_project(self, api_client):
        """Test retrieving a project that doesn't exist."""
        url = '/api/projects/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_project(self, api_client):
        """Test creating a new project."""
        url = '/api/projects/'
        data = {
            'title': 'New Project',
            'description': 'New project description',
            'shortDescription': 'Brief summary',
            'url': 'https://newproject.com',
            'githubUrl': 'https://github.com/user/new-repo',
            'technologies': 'Python, FastAPI',
            'isFeatured': True,
            'order': 2
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Project'
        assert response.data['description'] == 'New project description'
        assert response.data['isFeatured'] is True
        assert Project.objects.count() == 1

    def test_create_project_missing_title(self, api_client):
        """Test creating a project without required title field."""
        url = '/api/projects/'
        data = {
            'description': 'Project without title'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data

    def test_create_project_missing_description(self, api_client):
        """Test creating a project without required description field."""
        url = '/api/projects/'
        data = {
            'title': 'Project without description'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'description' in response.data

    def test_create_project_invalid_url(self, api_client):
        """Test creating a project with invalid URL."""
        url = '/api/projects/'
        data = {
            'title': 'Invalid URL Project',
            'description': 'Testing invalid URL',
            'url': 'not-a-valid-url'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'url' in response.data

    def test_update_project_full(self, api_client, sample_project):
        """Test full update of a project (PUT)."""
        url = f'/api/projects/{sample_project.id}/'
        data = {
            'title': 'Updated Project',
            'description': 'Updated description',
            'shortDescription': 'Updated summary',
            'url': 'https://updated.com',
            'githubUrl': 'https://github.com/updated/repo',
            'technologies': 'Python, Flask',
            'isFeatured': True,
            'order': 5
        }

        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Project'
        assert response.data['description'] == 'Updated description'
        assert response.data['order'] == 5

    def test_partial_update_project(self, api_client, sample_project):
        """Test partial update of a project (PATCH)."""
        url = f'/api/projects/{sample_project.id}/'
        data = {
            'title': 'Partially Updated Title'
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Partially Updated Title'
        assert response.data['description'] == 'Sample description'  # Unchanged

    def test_delete_project(self, api_client, sample_project):
        """Test deleting a project."""
        project_id = sample_project.id
        url = f'/api/projects/{project_id}/'

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Project.objects.filter(id=project_id).exists()

    def test_featured_projects_action(self, api_client, sample_project, featured_project):
        """Test the featured custom action to retrieve only featured projects."""
        url = '/api/projects/featured/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == featured_project.id
        assert response.data[0]['isFeatured'] is True

    def test_featured_projects_action_empty(self, api_client, sample_project):
        """Test featured action when no projects are featured."""
        url = '/api/projects/featured/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_search_projects_by_title(self, api_client):
        """Test searching projects by title."""
        Project.objects.create(title='Django Portfolio', description='Django app')
        Project.objects.create(title='React Frontend', description='React app')

        url = '/api/projects/?search=Django'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Django Portfolio'

    def test_search_projects_by_description(self, api_client):
        """Test searching projects by description."""
        Project.objects.create(title='Project A', description='Python backend service')
        Project.objects.create(title='Project B', description='JavaScript frontend')

        url = '/api/projects/?search=Python'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Project A'

    def test_search_projects_by_technologies(self, api_client):
        """Test searching projects by technologies."""
        Project.objects.create(
            title='Backend API',
            description='REST API',
            technologies='Django, PostgreSQL'
        )
        Project.objects.create(
            title='Frontend App',
            description='Web app',
            technologies='React, Redux'
        )

        url = '/api/projects/?search=Django'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Backend API'

    def test_order_projects_by_order_field(self, api_client):
        """Test ordering projects by order field."""
        Project.objects.create(title='Project C', description='Desc C', order=3)
        Project.objects.create(title='Project A', description='Desc A', order=1)
        Project.objects.create(title='Project B', description='Desc B', order=2)

        url = '/api/projects/?ordering=order'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['title'] == 'Project A'
        assert response.data[1]['title'] == 'Project B'
        assert response.data[2]['title'] == 'Project C'

    def test_order_projects_by_created_at_desc(self, api_client):
        """Test ordering projects by created_at descending."""
        project1 = Project.objects.create(title='First', description='Desc 1')
        project2 = Project.objects.create(title='Second', description='Desc 2')
        project3 = Project.objects.create(title='Third', description='Desc 3')

        url = '/api/projects/?ordering=-created_at'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Most recent first
        assert response.data[0]['title'] == 'Third'
        assert response.data[2]['title'] == 'First'

    def test_order_projects_by_title(self, api_client):
        """Test ordering projects by title alphabetically."""
        Project.objects.create(title='Zebra Project', description='Z project')
        Project.objects.create(title='Alpha Project', description='A project')
        Project.objects.create(title='Beta Project', description='B project')

        url = '/api/projects/?ordering=title'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['title'] == 'Alpha Project'
        assert response.data[1]['title'] == 'Beta Project'
        assert response.data[2]['title'] == 'Zebra Project'

    def test_default_ordering(self, api_client):
        """Test default ordering (order field, then -created_at)."""
        project1 = Project.objects.create(title='Order 2', description='Desc', order=2)
        project2 = Project.objects.create(title='Order 1 Old', description='Desc', order=1)
        project3 = Project.objects.create(title='Order 1 New', description='Desc', order=1)

        url = '/api/projects/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Order 1 projects first (most recent first), then order 2
        assert response.data[0]['order'] == 1
        assert response.data[1]['order'] == 1
        assert response.data[2]['order'] == 2

    def test_combined_search_and_ordering(self, api_client):
        """Test combining search and ordering."""
        Project.objects.create(title='Django App Z', description='Django', order=2)
        Project.objects.create(title='Django App A', description='Django', order=1)
        Project.objects.create(title='React App', description='React', order=1)

        url = '/api/projects/?search=Django&ordering=title'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['title'] == 'Django App A'
        assert response.data[1]['title'] == 'Django App Z'

    def test_response_field_names_camelcase(self, api_client, sample_project):
        """Test that API responses use camelCase field names."""
        url = f'/api/projects/{sample_project.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'shortDescription' in response.data
        assert 'imageUrl' in response.data
        assert 'githubUrl' in response.data
        assert 'isFeatured' in response.data
        assert 'createdAt' in response.data
        assert 'updatedAt' in response.data

    def test_create_multiple_featured_projects(self, api_client):
        """Test that multiple projects can be marked as featured."""
        url = '/api/projects/'

        data1 = {
            'title': 'Featured 1',
            'description': 'First featured',
            'isFeatured': True
        }
        data2 = {
            'title': 'Featured 2',
            'description': 'Second featured',
            'isFeatured': True
        }

        api_client.post(url, data1, format='json')
        api_client.post(url, data2, format='json')

        featured_url = '/api/projects/featured/'
        response = api_client.get(featured_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_update_project_to_featured(self, api_client, sample_project):
        """Test updating a regular project to be featured."""
        url = f'/api/projects/{sample_project.id}/'
        data = {'isFeatured': True}

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isFeatured'] is True

        # Verify it appears in featured endpoint
        featured_url = '/api/projects/featured/'
        featured_response = api_client.get(featured_url)
        assert len(featured_response.data) == 1

    def test_api_content_type_json(self, api_client, sample_project):
        """Test that API responses have JSON content type."""
        url = f'/api/projects/{sample_project.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']

    def test_project_not_found_returns_404(self, api_client):
        """Test that requesting non-existent project returns 404."""
        url = '/api/projects/12345/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
