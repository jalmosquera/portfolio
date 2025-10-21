"""
Tests for Skill and SkillCategory API views.
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.skills.models import Skill, SkillCategory


@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()


@pytest.fixture
def sample_category():
    """Fixture for creating a sample category."""
    return SkillCategory.objects.create(
        name='Programming',
        description='Programming languages',
        order=1
    )


@pytest.fixture
def sample_skill(sample_category):
    """Fixture for creating a sample skill."""
    return Skill.objects.create(
        name='Python',
        category=sample_category,
        proficiency='expert',
        percentage=90,
        years_experience=5,
        is_featured=False,
        order=1
    )


@pytest.fixture
def featured_skill(sample_category):
    """Fixture for creating a featured skill."""
    return Skill.objects.create(
        name='Django',
        category=sample_category,
        proficiency='advanced',
        percentage=85,
        is_featured=True,
        order=0
    )


@pytest.mark.django_db
class TestSkillViewSet:
    """Test suite for SkillViewSet."""

    def test_list_skills(self, api_client, sample_skill):
        """Test retrieving list of all skills."""
        url = '/api/skills/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Python'

    def test_list_skills_empty(self, api_client):
        """Test retrieving empty list when no skills exist."""
        url = '/api/skills/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_list_multiple_skills(self, api_client, sample_skill, featured_skill):
        """Test retrieving list with multiple skills."""
        url = '/api/skills/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_skill(self, api_client, sample_skill):
        """Test retrieving a single skill by ID."""
        url = f'/api/skills/{sample_skill.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_skill.id
        assert response.data['name'] == 'Python'
        assert response.data['proficiency'] == 'expert'
        assert response.data['percentage'] == 90

    def test_retrieve_nonexistent_skill(self, api_client):
        """Test retrieving a skill that doesn't exist."""
        url = '/api/skills/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_skill(self, api_client, sample_category):
        """Test creating a new skill."""
        url = '/api/skills/'
        data = {
            'name': 'JavaScript',
            'categoryId': sample_category.id,
            'proficiency': 'advanced',
            'percentage': 80,
            'icon': 'fab fa-js',
            'description': 'JavaScript programming language',
            'yearsExperience': 4,
            'isFeatured': True,
            'order': 2
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'JavaScript'
        assert response.data['proficiency'] == 'advanced'
        assert response.data['percentage'] == 80
        assert Skill.objects.count() == 1

    def test_create_skill_missing_required_name(self, api_client, sample_category):
        """Test creating a skill without required name field."""
        url = '/api/skills/'
        data = {
            'categoryId': sample_category.id,
            'yearsExperience': 0
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_create_skill_missing_required_category(self, api_client):
        """Test creating a skill without required category field."""
        url = '/api/skills/'
        data = {
            'name': 'Skill without category',
            'yearsExperience': 0
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'categoryId' in response.data

    def test_create_skill_invalid_proficiency(self, api_client, sample_category):
        """Test creating a skill with invalid proficiency."""
        url = '/api/skills/'
        data = {
            'name': 'Invalid Skill',
            'categoryId': sample_category.id,
            'proficiency': 'master',
            'yearsExperience': 0
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'proficiency' in response.data

    def test_update_skill_full(self, api_client, sample_skill):
        """Test full update of a skill (PUT)."""
        url = f'/api/skills/{sample_skill.id}/'
        data = {
            'name': 'Python Updated',
            'categoryId': sample_skill.category.id,
            'proficiency': 'expert',
            'percentage': 95,
            'icon': 'fab fa-python-updated',
            'description': 'Updated description',
            'yearsExperience': 6,
            'isFeatured': True,
            'order': 2
        }

        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Python Updated'
        assert response.data['percentage'] == 95
        assert response.data['isFeatured'] is True

    def test_partial_update_skill(self, api_client, sample_skill):
        """Test partial update of a skill (PATCH)."""
        url = f'/api/skills/{sample_skill.id}/'
        data = {
            'percentage': 95
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['percentage'] == 95
        assert response.data['name'] == 'Python'  # Unchanged

    def test_delete_skill(self, api_client, sample_skill):
        """Test deleting a skill."""
        skill_id = sample_skill.id
        url = f'/api/skills/{skill_id}/'

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Skill.objects.filter(id=skill_id).exists()

    def test_featured_skills_action(self, api_client, sample_skill, featured_skill):
        """Test the featured custom action to retrieve only featured skills."""
        url = '/api/skills/featured/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == featured_skill.id
        assert response.data[0]['isFeatured'] is True

    def test_featured_skills_action_empty(self, api_client, sample_skill):
        """Test featured action when no skills are featured."""
        url = '/api/skills/featured/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_by_category_action(self, api_client, sample_category, sample_skill):
        """Test the by_category custom action."""
        url = '/api/skills/by_category/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Programming'
        assert 'skills' in response.data[0]
        assert len(response.data[0]['skills']) == 1

    def test_by_category_action_multiple_categories(self, api_client):
        """Test by_category action with multiple categories."""
        cat1 = SkillCategory.objects.create(name='Frontend', order=1)
        cat2 = SkillCategory.objects.create(name='Backend', order=2)

        Skill.objects.create(name='React', category=cat1)
        Skill.objects.create(name='Django', category=cat2)
        Skill.objects.create(name='Python', category=cat2)

        url = '/api/skills/by_category/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        # Check that skills are nested in categories
        backend_cat = next(cat for cat in response.data if cat['name'] == 'Backend')
        assert len(backend_cat['skills']) == 2

    def test_search_skills_by_name(self, api_client, sample_category):
        """Test searching skills by name."""
        Skill.objects.create(name='Python', category=sample_category)
        Skill.objects.create(name='JavaScript', category=sample_category)

        url = '/api/skills/?search=Python'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Python'

    def test_search_skills_by_description(self, api_client, sample_category):
        """Test searching skills by description."""
        Skill.objects.create(
            name='Skill A',
            category=sample_category,
            description='Python programming'
        )
        Skill.objects.create(
            name='Skill B',
            category=sample_category,
            description='JavaScript development'
        )

        url = '/api/skills/?search=Python'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Skill A'

    def test_order_skills_by_order_field(self, api_client, sample_category):
        """Test ordering skills by order field."""
        Skill.objects.create(name='Skill C', category=sample_category, order=3)
        Skill.objects.create(name='Skill A', category=sample_category, order=1)
        Skill.objects.create(name='Skill B', category=sample_category, order=2)

        url = '/api/skills/?ordering=order'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == 'Skill A'
        assert response.data[1]['name'] == 'Skill B'
        assert response.data[2]['name'] == 'Skill C'

    def test_order_skills_by_name(self, api_client, sample_category):
        """Test ordering skills by name alphabetically."""
        Skill.objects.create(name='Zebra', category=sample_category)
        Skill.objects.create(name='Alpha', category=sample_category)
        Skill.objects.create(name='Beta', category=sample_category)

        url = '/api/skills/?ordering=name'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == 'Alpha'
        assert response.data[1]['name'] == 'Beta'
        assert response.data[2]['name'] == 'Zebra'

    def test_order_skills_by_percentage(self, api_client, sample_category):
        """Test ordering skills by percentage."""
        Skill.objects.create(name='Low', category=sample_category, percentage=30)
        Skill.objects.create(name='High', category=sample_category, percentage=90)
        Skill.objects.create(name='Medium', category=sample_category, percentage=60)

        url = '/api/skills/?ordering=percentage'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['percentage'] == 30
        assert response.data[1]['percentage'] == 60
        assert response.data[2]['percentage'] == 90

    def test_default_ordering(self, api_client):
        """Test default ordering (category order, skill order, name)."""
        cat1 = SkillCategory.objects.create(name='Cat1', order=1)
        cat2 = SkillCategory.objects.create(name='Cat2', order=2)

        skill1 = Skill.objects.create(name='B Skill', category=cat1, order=2)
        skill2 = Skill.objects.create(name='A Skill', category=cat1, order=1)
        skill3 = Skill.objects.create(name='C Skill', category=cat2, order=1)

        url = '/api/skills/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Cat1 skills first (by order), then cat2
        assert response.data[0]['name'] == 'A Skill'
        assert response.data[1]['name'] == 'B Skill'
        assert response.data[2]['name'] == 'C Skill'

    def test_response_field_names_camelcase(self, api_client, sample_skill):
        """Test that API responses use camelCase field names."""
        url = f'/api/skills/{sample_skill.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'categoryId' in response.data
        assert 'categoryName' in response.data
        assert 'yearsExperience' in response.data
        assert 'isFeatured' in response.data
        assert 'createdAt' in response.data
        assert 'updatedAt' in response.data

    def test_api_content_type_json(self, api_client, sample_skill):
        """Test that API responses have JSON content type."""
        url = f'/api/skills/{sample_skill.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']

    def test_create_multiple_featured_skills(self, api_client, sample_category):
        """Test that multiple skills can be marked as featured."""
        url = '/api/skills/'

        data1 = {
            'name': 'Featured 1',
            'categoryId': sample_category.id,
            'isFeatured': True,
            'yearsExperience': 0
        }
        data2 = {
            'name': 'Featured 2',
            'categoryId': sample_category.id,
            'isFeatured': True,
            'yearsExperience': 0
        }

        api_client.post(url, data1, format='json')
        api_client.post(url, data2, format='json')

        featured_url = '/api/skills/featured/'
        response = api_client.get(featured_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.django_db
class TestSkillCategoryViewSet:
    """Test suite for SkillCategoryViewSet."""

    def test_list_categories(self, api_client, sample_category):
        """Test retrieving list of all categories."""
        url = '/api/skill-categories/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Programming'

    def test_list_categories_empty(self, api_client):
        """Test retrieving empty list when no categories exist."""
        url = '/api/skill-categories/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_retrieve_category(self, api_client, sample_category):
        """Test retrieving a single category by ID."""
        url = f'/api/skill-categories/{sample_category.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_category.id
        assert response.data['name'] == 'Programming'

    def test_retrieve_category_with_skills(self, api_client, sample_category, sample_skill):
        """Test retrieving a category includes its skills."""
        url = f'/api/skill-categories/{sample_category.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'skills' in response.data
        assert len(response.data['skills']) == 1
        assert response.data['skills'][0]['name'] == 'Python'

    def test_retrieve_nonexistent_category(self, api_client):
        """Test retrieving a category that doesn't exist."""
        url = '/api/skill-categories/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_category(self, api_client):
        """Test creating a new category."""
        url = '/api/skill-categories/'
        data = {
            'name': 'Web Development',
            'description': 'Web development technologies',
            'order': 1
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Web Development'
        assert response.data['description'] == 'Web development technologies'
        assert SkillCategory.objects.count() == 1

    def test_create_category_missing_required_name(self, api_client):
        """Test creating a category without required name field."""
        url = '/api/skill-categories/'
        data = {
            'description': 'Description without name'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_update_category_full(self, api_client, sample_category):
        """Test full update of a category (PUT)."""
        url = f'/api/skill-categories/{sample_category.id}/'
        data = {
            'name': 'Updated Programming',
            'description': 'Updated description',
            'order': 2
        }

        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Programming'
        assert response.data['order'] == 2

    def test_partial_update_category(self, api_client, sample_category):
        """Test partial update of a category (PATCH)."""
        url = f'/api/skill-categories/{sample_category.id}/'
        data = {
            'description': 'Partially updated description'
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == 'Partially updated description'
        assert response.data['name'] == 'Programming'  # Unchanged

    def test_delete_category(self, api_client, sample_category):
        """Test deleting a category."""
        category_id = sample_category.id
        url = f'/api/skill-categories/{category_id}/'

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not SkillCategory.objects.filter(id=category_id).exists()

    def test_delete_category_cascades_to_skills(self, api_client, sample_category, sample_skill):
        """Test that deleting a category also deletes its skills."""
        skill_id = sample_skill.id
        category_id = sample_category.id

        url = f'/api/skill-categories/{category_id}/'
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not SkillCategory.objects.filter(id=category_id).exists()
        assert not Skill.objects.filter(id=skill_id).exists()

    def test_list_categories_ordering(self, api_client):
        """Test that categories are ordered by order field, then name."""
        SkillCategory.objects.create(name='Z Category', order=2)
        SkillCategory.objects.create(name='A Category', order=1)
        SkillCategory.objects.create(name='B Category', order=1)

        url = '/api/skill-categories/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == 'A Category'
        assert response.data[1]['name'] == 'B Category'
        assert response.data[2]['name'] == 'Z Category'

    def test_response_field_names_camelcase(self, api_client, sample_category):
        """Test that API responses use camelCase field names."""
        url = f'/api/skill-categories/{sample_category.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'createdAt' in response.data
        assert 'updatedAt' in response.data

    def test_api_content_type_json(self, api_client, sample_category):
        """Test that API responses have JSON content type."""
        url = f'/api/skill-categories/{sample_category.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']

    def test_category_not_found_returns_404(self, api_client):
        """Test that requesting non-existent category returns 404."""
        url = '/api/skill-categories/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_multiple_categories_with_skills(self, api_client):
        """Test listing multiple categories each with their skills."""
        cat1 = SkillCategory.objects.create(name='Frontend')
        cat2 = SkillCategory.objects.create(name='Backend')

        Skill.objects.create(name='React', category=cat1)
        Skill.objects.create(name='Vue', category=cat1)
        Skill.objects.create(name='Django', category=cat2)

        url = '/api/skill-categories/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        frontend = next(cat for cat in response.data if cat['name'] == 'Frontend')
        backend = next(cat for cat in response.data if cat['name'] == 'Backend')

        assert len(frontend['skills']) == 2
        assert len(backend['skills']) == 1
