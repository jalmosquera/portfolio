"""
Tests for Skill and SkillCategory models.
"""

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.skills.models import Skill, SkillCategory


@pytest.mark.django_db
class TestSkillCategoryModel:
    """Test suite for SkillCategory model."""

    def test_create_skill_category_with_required_fields(self):
        """Test creating a skill category with only required fields."""
        category = SkillCategory.objects.create(
            name="Programming Languages"
        )

        assert category.id is not None
        assert category.name == "Programming Languages"
        assert category.description == ""
        assert category.order == 0
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_create_skill_category_with_all_fields(self):
        """Test creating a skill category with all fields populated."""
        category = SkillCategory.objects.create(
            name="Web Development",
            description="Technologies and frameworks for web development",
            order=1
        )

        assert category.name == "Web Development"
        assert category.description == "Technologies and frameworks for web development"
        assert category.order == 1

    def test_skill_category_str_representation(self):
        """Test the string representation of a skill category."""
        category = SkillCategory.objects.create(
            name="Backend Technologies"
        )

        assert str(category) == "Backend Technologies"

    def test_skill_category_ordering_default(self):
        """Test that categories are ordered by order field, then name."""
        category1 = SkillCategory.objects.create(name="Z Category", order=2)
        category2 = SkillCategory.objects.create(name="A Category", order=1)
        category3 = SkillCategory.objects.create(name="B Category", order=1)

        categories = list(SkillCategory.objects.all())

        # Categories with order=1 should come first, alphabetically
        assert categories[0].name == "A Category"
        assert categories[1].name == "B Category"
        assert categories[2].name == "Z Category"

    def test_category_name_max_length(self):
        """Test that name field respects max_length constraint."""
        long_name = "x" * 101  # Exceeds max_length of 100

        category = SkillCategory(name=long_name)

        with pytest.raises(ValidationError):
            category.full_clean()

    def test_category_description_blank_allowed(self):
        """Test that description field can be blank."""
        category = SkillCategory.objects.create(
            name="Minimal Category",
            description=""
        )

        category.full_clean()  # Should not raise validation error
        assert category.description == ""

    def test_category_order_default_zero(self):
        """Test that order field defaults to 0."""
        category = SkillCategory.objects.create(name="Default Order")

        assert category.order == 0

    def test_category_created_at_auto_set(self):
        """Test that created_at is automatically set on creation."""
        before = timezone.now()
        category = SkillCategory.objects.create(name="Timestamp Test")
        after = timezone.now()

        assert before <= category.created_at <= after

    def test_category_updated_at_auto_updates(self):
        """Test that updated_at is automatically updated on save."""
        category = SkillCategory.objects.create(name="Update Test")

        original_updated = category.updated_at

        import time
        time.sleep(0.01)

        category.name = "Updated Name"
        category.save()

        assert category.updated_at > original_updated

    def test_category_meta_verbose_names(self):
        """Test the Meta class verbose names."""
        assert SkillCategory._meta.verbose_name == "Skill Category"
        assert SkillCategory._meta.verbose_name_plural == "Skill Categories"


@pytest.mark.django_db
class TestSkillModel:
    """Test suite for Skill model."""

    @pytest.fixture
    def sample_category(self):
        """Fixture for creating a sample skill category."""
        return SkillCategory.objects.create(
            name="Programming",
            description="Programming languages",
            order=1
        )

    def test_create_skill_with_required_fields(self, sample_category):
        """Test creating a skill with only required fields."""
        skill = Skill.objects.create(
            name="Python",
            category=sample_category
        )

        assert skill.id is not None
        assert skill.name == "Python"
        assert skill.category == sample_category
        assert skill.proficiency == "intermediate"
        assert skill.percentage == 50
        assert skill.icon == ""
        assert skill.description == ""
        assert skill.years_experience == 0
        assert skill.is_featured is False
        assert skill.order == 0
        assert skill.created_at is not None
        assert skill.updated_at is not None

    def test_create_skill_with_all_fields(self, sample_category):
        """Test creating a skill with all fields populated."""
        skill = Skill.objects.create(
            name="Django",
            category=sample_category,
            proficiency="expert",
            percentage=95,
            icon="fab fa-python",
            description="Django web framework for Python",
            years_experience=5,
            is_featured=True,
            order=1
        )

        assert skill.name == "Django"
        assert skill.proficiency == "expert"
        assert skill.percentage == 95
        assert skill.icon == "fab fa-python"
        assert skill.description == "Django web framework for Python"
        assert skill.years_experience == 5
        assert skill.is_featured is True
        assert skill.order == 1

    def test_skill_str_representation(self, sample_category):
        """Test the string representation of a skill."""
        skill = Skill.objects.create(
            name="JavaScript",
            category=sample_category
        )

        assert str(skill) == "JavaScript (Programming)"

    def test_skill_ordering_default(self):
        """Test that skills are ordered by category order, skill order, then name."""
        category1 = SkillCategory.objects.create(name="Category 1", order=1)
        category2 = SkillCategory.objects.create(name="Category 2", order=2)

        skill1 = Skill.objects.create(name="Skill C", category=category1, order=2)
        skill2 = Skill.objects.create(name="Skill A", category=category1, order=1)
        skill3 = Skill.objects.create(name="Skill B", category=category2, order=1)

        skills = list(Skill.objects.all())

        # Category 1 skills first (by order), then category 2
        assert skills[0].name == "Skill A"
        assert skills[1].name == "Skill C"
        assert skills[2].name == "Skill B"

    def test_skill_proficiency_choices(self, sample_category):
        """Test that proficiency field accepts valid choices."""
        valid_choices = ['beginner', 'intermediate', 'advanced', 'expert']

        for choice in valid_choices:
            skill = Skill.objects.create(
                name=f"Skill {choice}",
                category=sample_category,
                proficiency=choice
            )
            assert skill.proficiency == choice

    def test_skill_proficiency_invalid_choice(self, sample_category):
        """Test that proficiency field rejects invalid choices."""
        skill = Skill(
            name="Invalid Proficiency",
            category=sample_category,
            proficiency="master"  # Invalid choice
        )

        with pytest.raises(ValidationError):
            skill.full_clean()

    def test_skill_percentage_validation(self, sample_category):
        """Test that percentage field validates range 0-100."""
        # Valid percentages
        for pct in [0, 50, 100]:
            skill = Skill.objects.create(
                name=f"Skill {pct}",
                category=sample_category,
                percentage=pct
            )
            skill.full_clean()  # Should not raise
            assert skill.percentage == pct

    def test_skill_percentage_below_minimum(self, sample_category):
        """Test that percentage below 0 is invalid."""
        skill = Skill(
            name="Invalid Low",
            category=sample_category,
            percentage=-1
        )

        with pytest.raises(ValidationError):
            skill.full_clean()

    def test_skill_percentage_above_maximum(self, sample_category):
        """Test that percentage above 100 is invalid."""
        skill = Skill(
            name="Invalid High",
            category=sample_category,
            percentage=101
        )

        with pytest.raises(ValidationError):
            skill.full_clean()

    def test_skill_years_experience_validation(self, sample_category):
        """Test that years_experience validates non-negative."""
        skill = Skill.objects.create(
            name="Valid Experience",
            category=sample_category,
            years_experience=10
        )

        skill.full_clean()  # Should not raise
        assert skill.years_experience == 10

    def test_skill_years_experience_negative(self, sample_category):
        """Test that negative years_experience is invalid."""
        skill = Skill(
            name="Invalid Experience",
            category=sample_category,
            years_experience=-1
        )

        with pytest.raises(ValidationError):
            skill.full_clean()

    def test_skill_name_max_length(self, sample_category):
        """Test that name field respects max_length constraint."""
        long_name = "x" * 101  # Exceeds max_length of 100

        skill = Skill(
            name=long_name,
            category=sample_category
        )

        with pytest.raises(ValidationError):
            skill.full_clean()

    def test_skill_icon_max_length(self, sample_category):
        """Test that icon field respects max_length constraint."""
        long_icon = "x" * 101  # Exceeds max_length of 100

        skill = Skill(
            name="Icon Test",
            category=sample_category,
            icon=long_icon
        )

        with pytest.raises(ValidationError):
            skill.full_clean()

    def test_skill_description_blank_allowed(self, sample_category):
        """Test that description field can be blank."""
        skill = Skill.objects.create(
            name="No Description",
            category=sample_category,
            description=""
        )

        skill.full_clean()  # Should not raise validation error
        assert skill.description == ""

    def test_skill_icon_blank_allowed(self, sample_category):
        """Test that icon field can be blank."""
        skill = Skill.objects.create(
            name="No Icon",
            category=sample_category,
            icon=""
        )

        skill.full_clean()  # Should not raise validation error
        assert skill.icon == ""

    def test_skill_created_at_auto_set(self, sample_category):
        """Test that created_at is automatically set on creation."""
        before = timezone.now()
        skill = Skill.objects.create(
            name="Timestamp Test",
            category=sample_category
        )
        after = timezone.now()

        assert before <= skill.created_at <= after

    def test_skill_updated_at_auto_updates(self, sample_category):
        """Test that updated_at is automatically updated on save."""
        skill = Skill.objects.create(
            name="Update Test",
            category=sample_category
        )

        original_updated = skill.updated_at

        import time
        time.sleep(0.01)

        skill.name = "Updated Name"
        skill.save()

        assert skill.updated_at > original_updated

    def test_skill_is_featured_default_false(self, sample_category):
        """Test that is_featured defaults to False."""
        skill = Skill.objects.create(
            name="Featured Test",
            category=sample_category
        )

        assert skill.is_featured is False

    def test_skill_order_default_zero(self, sample_category):
        """Test that order defaults to 0."""
        skill = Skill.objects.create(
            name="Order Test",
            category=sample_category
        )

        assert skill.order == 0

    def test_skill_proficiency_default(self, sample_category):
        """Test that proficiency defaults to 'intermediate'."""
        skill = Skill.objects.create(
            name="Proficiency Default",
            category=sample_category
        )

        assert skill.proficiency == "intermediate"

    def test_skill_percentage_default(self, sample_category):
        """Test that percentage defaults to 50."""
        skill = Skill.objects.create(
            name="Percentage Default",
            category=sample_category
        )

        assert skill.percentage == 50

    def test_skill_years_experience_default(self, sample_category):
        """Test that years_experience defaults to 0."""
        skill = Skill.objects.create(
            name="Experience Default",
            category=sample_category
        )

        assert skill.years_experience == 0

    def test_skill_category_foreign_key(self, sample_category):
        """Test that skill has proper foreign key relationship with category."""
        skill = Skill.objects.create(
            name="FK Test",
            category=sample_category
        )

        assert skill.category.id == sample_category.id
        assert skill.category.name == "Programming"

    def test_skill_category_cascade_delete(self, sample_category):
        """Test that deleting a category cascades to its skills."""
        skill = Skill.objects.create(
            name="Cascade Test",
            category=sample_category
        )

        skill_id = skill.id
        sample_category.delete()

        assert not Skill.objects.filter(id=skill_id).exists()

    def test_skill_category_related_name(self, sample_category):
        """Test accessing skills through category's related_name."""
        skill1 = Skill.objects.create(name="Skill 1", category=sample_category)
        skill2 = Skill.objects.create(name="Skill 2", category=sample_category)

        category_skills = sample_category.skills.all()

        assert category_skills.count() == 2
        assert skill1 in category_skills
        assert skill2 in category_skills

    def test_filter_featured_skills(self, sample_category):
        """Test filtering skills by is_featured flag."""
        Skill.objects.create(
            name="Regular Skill",
            category=sample_category,
            is_featured=False
        )
        featured_skill = Skill.objects.create(
            name="Featured Skill",
            category=sample_category,
            is_featured=True
        )

        featured_skills = Skill.objects.filter(is_featured=True)

        assert featured_skills.count() == 1
        assert featured_skills.first() == featured_skill

    def test_skill_meta_verbose_names(self):
        """Test the Meta class verbose names."""
        assert Skill._meta.verbose_name == "Skill"
        assert Skill._meta.verbose_name_plural == "Skills"

    def test_multiple_skills_same_category(self, sample_category):
        """Test creating multiple skills in the same category."""
        skill1 = Skill.objects.create(name="Python", category=sample_category)
        skill2 = Skill.objects.create(name="Java", category=sample_category)
        skill3 = Skill.objects.create(name="C++", category=sample_category)

        category_skills = sample_category.skills.all()

        assert category_skills.count() == 3

    def test_skill_percentage_boundary_values(self, sample_category):
        """Test percentage field boundary values."""
        # Test minimum boundary
        skill_min = Skill.objects.create(
            name="Min Percentage",
            category=sample_category,
            percentage=0
        )
        skill_min.full_clean()
        assert skill_min.percentage == 0

        # Test maximum boundary
        skill_max = Skill.objects.create(
            name="Max Percentage",
            category=sample_category,
            percentage=100
        )
        skill_max.full_clean()
        assert skill_max.percentage == 100

    def test_skill_years_experience_zero(self, sample_category):
        """Test that years_experience can be 0."""
        skill = Skill.objects.create(
            name="Zero Experience",
            category=sample_category,
            years_experience=0
        )

        skill.full_clean()
        assert skill.years_experience == 0

    def test_skill_all_proficiency_levels(self, sample_category):
        """Test creating skills with all proficiency levels."""
        proficiency_levels = {
            'beginner': 'Beginner Skill',
            'intermediate': 'Intermediate Skill',
            'advanced': 'Advanced Skill',
            'expert': 'Expert Skill'
        }

        for level, name in proficiency_levels.items():
            skill = Skill.objects.create(
                name=name,
                category=sample_category,
                proficiency=level
            )
            assert skill.proficiency == level

        assert Skill.objects.count() == 4
