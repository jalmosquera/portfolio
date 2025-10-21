"""
Tests for Skill and SkillCategory serializers.
"""

import pytest
from apps.skills.models import Skill, SkillCategory
from apps.skills.api.serializers import SkillSerializer, SkillCategorySerializer


@pytest.mark.django_db
class TestSkillCategorySerializer:
    """Test suite for SkillCategorySerializer."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid data."""
        data = {
            'name': 'Web Development',
            'description': 'Web development technologies',
            'order': 1
        }

        serializer = SkillCategorySerializer(data=data)
        assert serializer.is_valid()
        category = serializer.save()

        assert category.name == 'Web Development'
        assert category.description == 'Web development technologies'
        assert category.order == 1

    def test_serializer_with_minimal_data(self):
        """Test serializer with only required fields."""
        data = {
            'name': 'Backend'
        }

        serializer = SkillCategorySerializer(data=data)
        assert serializer.is_valid()
        category = serializer.save()

        assert category.name == 'Backend'
        assert category.description == ''
        assert category.order == 0

    def test_serializer_missing_required_name(self):
        """Test serializer validation fails when name is missing."""
        data = {
            'description': 'Description without name'
        }

        serializer = SkillCategorySerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_serializer_camelcase_field_mapping(self):
        """Test that camelCase fields map correctly."""
        category = SkillCategory.objects.create(
            name='Test Category',
            description='Test description'
        )

        serializer = SkillCategorySerializer(category)

        assert 'createdAt' in serializer.data
        assert 'updatedAt' in serializer.data

    def test_serializer_includes_nested_skills(self):
        """Test that serializer includes related skills."""
        category = SkillCategory.objects.create(name='Programming')
        Skill.objects.create(name='Python', category=category)
        Skill.objects.create(name='Java', category=category)

        serializer = SkillCategorySerializer(category)

        assert 'skills' in serializer.data
        assert len(serializer.data['skills']) == 2

    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be modified."""
        category = SkillCategory.objects.create(name='Original')

        original_id = category.id
        original_created = category.created_at

        data = {
            'id': 99999,
            'name': 'Updated',
            'createdAt': '2020-01-01T00:00:00Z'
        }

        serializer = SkillCategorySerializer(category, data=data)
        assert serializer.is_valid()
        updated_category = serializer.save()

        assert updated_category.id == original_id
        assert updated_category.created_at == original_created
        assert updated_category.name == 'Updated'

    def test_serializer_output_structure(self):
        """Test that serializer output has all expected fields."""
        category = SkillCategory.objects.create(name='Test')

        serializer = SkillCategorySerializer(category)
        expected_fields = {
            'id', 'name', 'description', 'order',
            'skills', 'createdAt', 'updatedAt'
        }

        assert set(serializer.data.keys()) == expected_fields

    def test_serializer_partial_update(self):
        """Test partial update of a category."""
        category = SkillCategory.objects.create(
            name='Original',
            description='Original description',
            order=1
        )

        data = {'name': 'Updated'}

        serializer = SkillCategorySerializer(category, data=data, partial=True)
        assert serializer.is_valid()
        updated_category = serializer.save()

        assert updated_category.name == 'Updated'
        assert updated_category.description == 'Original description'
        assert updated_category.order == 1


@pytest.mark.django_db
class TestSkillSerializer:
    """Test suite for SkillSerializer."""

    @pytest.fixture
    def sample_category(self):
        """Fixture for creating a sample category."""
        return SkillCategory.objects.create(name='Programming')

    def test_serializer_with_valid_data(self, sample_category):
        """Test serializer with valid data."""
        data = {
            'name': 'Python',
            'categoryId': sample_category.id,
            'proficiency': 'expert',
            'percentage': 90,
            'icon': 'fab fa-python',
            'description': 'Python programming language',
            'yearsExperience': 5,
            'isFeatured': True,
            'order': 1
        }

        serializer = SkillSerializer(data=data)
        assert serializer.is_valid()
        skill = serializer.save()

        assert skill.name == 'Python'
        assert skill.category == sample_category
        assert skill.proficiency == 'expert'
        assert skill.percentage == 90
        assert skill.icon == 'fab fa-python'
        assert skill.description == 'Python programming language'
        assert skill.years_experience == 5
        assert skill.is_featured is True
        assert skill.order == 1

    def test_serializer_with_minimal_data(self, sample_category):
        """Test serializer with only required fields."""
        data = {
            'name': 'JavaScript',
            'categoryId': sample_category.id,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert serializer.is_valid()
        skill = serializer.save()

        assert skill.name == 'JavaScript'
        assert skill.category == sample_category
        assert skill.proficiency == 'intermediate'
        assert skill.percentage == 50

    def test_serializer_missing_required_name(self, sample_category):
        """Test serializer validation fails when name is missing."""
        data = {
            'categoryId': sample_category.id,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_serializer_missing_required_category(self):
        """Test serializer validation fails when category is missing."""
        data = {
            'name': 'Skill without category',
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()
        assert 'categoryId' in serializer.errors

    def test_serializer_invalid_category_id(self):
        """Test serializer validation fails with invalid category ID."""
        data = {
            'name': 'Invalid Category',
            'categoryId': 99999,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()
        assert 'categoryId' in serializer.errors

    def test_serializer_camelcase_field_mapping(self, sample_category):
        """Test that camelCase fields map correctly to snake_case."""
        skill = Skill.objects.create(
            name='Camel Test',
            category=sample_category,
            years_experience=3,
            is_featured=True
        )

        serializer = SkillSerializer(skill)

        assert 'categoryId' in serializer.data
        assert 'categoryName' in serializer.data
        assert 'yearsExperience' in serializer.data
        assert 'isFeatured' in serializer.data
        assert 'createdAt' in serializer.data
        assert 'updatedAt' in serializer.data

        assert serializer.data['categoryId'] == sample_category.id
        assert serializer.data['categoryName'] == 'Programming'
        assert serializer.data['yearsExperience'] == 3
        assert serializer.data['isFeatured'] is True

    def test_serializer_category_name_read_only(self, sample_category):
        """Test that categoryName is read-only."""
        skill = Skill.objects.create(
            name='Read-only Test',
            category=sample_category
        )

        data = {
            'name': 'Updated',
            'categoryId': sample_category.id,
            'categoryName': 'Should Not Update',
            'yearsExperience': 1
        }

        serializer = SkillSerializer(skill, data=data)
        assert serializer.is_valid()
        updated_skill = serializer.save()

        assert updated_skill.category.name == 'Programming'

    def test_serializer_read_only_fields(self, sample_category):
        """Test that read-only fields cannot be modified."""
        skill = Skill.objects.create(
            name='Read-only',
            category=sample_category
        )

        original_id = skill.id
        original_created = skill.created_at

        data = {
            'id': 99999,
            'name': 'Updated',
            'categoryId': sample_category.id,
            'categoryName': 'Ignored',
            'yearsExperience': 1,
            'createdAt': '2020-01-01T00:00:00Z'
        }

        serializer = SkillSerializer(skill, data=data)
        assert serializer.is_valid()
        updated_skill = serializer.save()

        assert updated_skill.id == original_id
        assert updated_skill.created_at == original_created

    def test_serializer_proficiency_validation(self, sample_category):
        """Test that proficiency field validates choices."""
        valid_choices = ['beginner', 'intermediate', 'advanced', 'expert']

        for choice in valid_choices:
            data = {
                'name': f'Skill {choice}',
                'categoryId': sample_category.id,
                'proficiency': choice,
                'yearsExperience': 0
            }

            serializer = SkillSerializer(data=data)
            assert serializer.is_valid()

    def test_serializer_invalid_proficiency(self, sample_category):
        """Test that invalid proficiency is rejected."""
        data = {
            'name': 'Invalid Proficiency',
            'categoryId': sample_category.id,
            'proficiency': 'master',
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()
        assert 'proficiency' in serializer.errors

    def test_serializer_percentage_validation(self, sample_category):
        """Test that percentage field validates range."""
        # Valid percentages
        for pct in [0, 50, 100]:
            data = {
                'name': f'Skill {pct}',
                'categoryId': sample_category.id,
                'percentage': pct,
                'yearsExperience': 0
            }

            serializer = SkillSerializer(data=data)
            assert serializer.is_valid()

    def test_serializer_invalid_percentage_low(self, sample_category):
        """Test that percentage below 0 is invalid."""
        data = {
            'name': 'Invalid Low',
            'categoryId': sample_category.id,
            'percentage': -1,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()

    def test_serializer_invalid_percentage_high(self, sample_category):
        """Test that percentage above 100 is invalid."""
        data = {
            'name': 'Invalid High',
            'categoryId': sample_category.id,
            'percentage': 101,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()

    def test_serializer_years_experience_validation(self, sample_category):
        """Test that years_experience validates non-negative."""
        data = {
            'name': 'Valid Experience',
            'categoryId': sample_category.id,
            'yearsExperience': 10
        }

        serializer = SkillSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_invalid_years_experience(self, sample_category):
        """Test that negative years_experience is invalid."""
        data = {
            'name': 'Invalid Experience',
            'categoryId': sample_category.id,
            'yearsExperience': -1
        }

        serializer = SkillSerializer(data=data)
        assert not serializer.is_valid()

    def test_serializer_output_structure(self, sample_category):
        """Test that serializer output has all expected fields."""
        skill = Skill.objects.create(
            name='Structure Test',
            category=sample_category
        )

        serializer = SkillSerializer(skill)
        expected_fields = {
            'id', 'name', 'categoryId', 'categoryName', 'proficiency',
            'percentage', 'icon', 'description', 'yearsExperience',
            'isFeatured', 'order', 'createdAt', 'updatedAt'
        }

        assert set(serializer.data.keys()) == expected_fields

    def test_serializer_partial_update(self, sample_category):
        """Test partial update of a skill."""
        skill = Skill.objects.create(
            name='Original',
            category=sample_category,
            percentage=50
        )

        data = {'percentage': 80}

        serializer = SkillSerializer(skill, data=data, partial=True)
        assert serializer.is_valid()
        updated_skill = serializer.save()

        assert updated_skill.percentage == 80
        assert updated_skill.name == 'Original'

    def test_serializer_toggle_featured(self, sample_category):
        """Test toggling isFeatured field."""
        skill = Skill.objects.create(
            name='Featured Test',
            category=sample_category,
            is_featured=False
        )

        data = {'isFeatured': True}
        serializer = SkillSerializer(skill, data=data, partial=True)
        assert serializer.is_valid()
        updated_skill = serializer.save()

        assert updated_skill.is_featured is True

    def test_serializer_update_category(self, sample_category):
        """Test updating skill's category."""
        new_category = SkillCategory.objects.create(name='New Category')
        skill = Skill.objects.create(
            name='Category Update Test',
            category=sample_category
        )

        data = {
            'name': 'Category Update Test',
            'categoryId': new_category.id,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(skill, data=data)
        assert serializer.is_valid()
        updated_skill = serializer.save()

        assert updated_skill.category == new_category

    def test_serializer_list_serialization(self, sample_category):
        """Test serializing multiple skills."""
        Skill.objects.create(name='Skill 1', category=sample_category)
        Skill.objects.create(name='Skill 2', category=sample_category)

        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)

        assert len(serializer.data) == 2

    def test_serializer_boolean_defaults(self, sample_category):
        """Test boolean field default values."""
        data = {
            'name': 'Boolean Test',
            'categoryId': sample_category.id,
            'yearsExperience': 0
        }

        serializer = SkillSerializer(data=data)
        assert serializer.is_valid()
        skill = serializer.save()

        assert skill.is_featured is False

    def test_serializer_with_all_proficiency_levels(self, sample_category):
        """Test creating skills with all proficiency levels."""
        proficiency_levels = ['beginner', 'intermediate', 'advanced', 'expert']

        for level in proficiency_levels:
            data = {
                'name': f'{level.capitalize()} Skill',
                'categoryId': sample_category.id,
                'proficiency': level,
                'yearsExperience': 0
            }

            serializer = SkillSerializer(data=data)
            assert serializer.is_valid()
            skill = serializer.save()
            assert skill.proficiency == level
