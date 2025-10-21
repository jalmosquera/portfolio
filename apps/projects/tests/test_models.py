"""
Tests for Project model.
"""

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.projects.models import Project


@pytest.mark.django_db
class TestProjectModel:
    """Test suite for Project model."""

    def test_create_project_with_required_fields(self):
        """Test creating a project with only required fields."""
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project description."
        )

        assert project.id is not None
        assert project.title == "Test Project"
        assert project.description == "This is a test project description."
        assert project.short_description == ""
        assert project.image.name == ""
        assert project.url == ""
        assert project.github_url == ""
        assert project.technologies == ""
        assert project.is_featured is False
        assert project.order == 0
        assert project.created_at is not None
        assert project.updated_at is not None

    def test_create_project_with_all_fields(self):
        """Test creating a project with all fields populated."""
        project = Project.objects.create(
            title="Full Featured Project",
            description="A comprehensive project description with all details.",
            short_description="Brief summary of the project",
            url="https://example.com/project",
            github_url="https://github.com/user/repo",
            technologies="Python, Django, PostgreSQL, React",
            is_featured=True,
            order=1
        )

        assert project.title == "Full Featured Project"
        assert project.description == "A comprehensive project description with all details."
        assert project.short_description == "Brief summary of the project"
        assert project.url == "https://example.com/project"
        assert project.github_url == "https://github.com/user/repo"
        assert project.technologies == "Python, Django, PostgreSQL, React"
        assert project.is_featured is True
        assert project.order == 1

    def test_project_str_representation(self):
        """Test the string representation of a project."""
        project = Project.objects.create(
            title="My Portfolio Project",
            description="Description here"
        )

        assert str(project) == "My Portfolio Project"

    def test_project_ordering_default(self):
        """Test that projects are ordered by order field, then by created_at descending."""
        project1 = Project.objects.create(
            title="Project 1",
            description="First project",
            order=2
        )
        project2 = Project.objects.create(
            title="Project 2",
            description="Second project",
            order=1
        )
        project3 = Project.objects.create(
            title="Project 3",
            description="Third project",
            order=1
        )

        projects = list(Project.objects.all())

        # Projects with order=1 should come first
        assert projects[0] in [project2, project3]
        assert projects[1] in [project2, project3]
        # Project with order=2 should come last
        assert projects[2] == project1

    def test_project_to_dict_method(self):
        """Test the to_dict method returns correct camelCase dictionary."""
        project = Project.objects.create(
            title="Dict Test Project",
            description="Testing to_dict method",
            short_description="Short desc",
            url="https://test.com",
            github_url="https://github.com/test",
            technologies="Python,Django,React",
            is_featured=True,
            order=5
        )

        result = project.to_dict()

        assert result["id"] == project.id
        assert result["title"] == "Dict Test Project"
        assert result["description"] == "Testing to_dict method"
        assert result["shortDescription"] == "Short desc"
        assert result["imageUrl"] is None
        assert result["url"] == "https://test.com"
        assert result["githubUrl"] == "https://github.com/test"
        assert result["technologies"] == ["Python", "Django", "React"]
        assert result["isFeatured"] is True
        assert result["order"] == 5
        assert result["createdAt"] is not None
        assert result["updatedAt"] is not None

    def test_project_to_dict_with_empty_technologies(self):
        """Test to_dict with empty technologies returns empty list."""
        project = Project.objects.create(
            title="No Tech Project",
            description="Project without technologies",
            technologies=""
        )

        result = project.to_dict()

        assert result["technologies"] == []

    def test_project_to_dict_with_no_technologies_field(self):
        """Test to_dict when technologies field is None."""
        project = Project.objects.create(
            title="Null Tech Project",
            description="Project with null technologies"
        )
        project.technologies = None

        result = project.to_dict()

        assert result["technologies"] == []

    def test_project_title_max_length(self):
        """Test that title field respects max_length constraint."""
        long_title = "x" * 201  # Exceeds max_length of 200

        project = Project(
            title=long_title,
            description="Test description"
        )

        with pytest.raises(ValidationError):
            project.full_clean()

    def test_project_short_description_max_length(self):
        """Test that short_description field respects max_length constraint."""
        long_short_desc = "x" * 301  # Exceeds max_length of 300

        project = Project(
            title="Test",
            description="Test description",
            short_description=long_short_desc
        )

        with pytest.raises(ValidationError):
            project.full_clean()

    def test_project_technologies_max_length(self):
        """Test that technologies field respects max_length constraint."""
        long_tech = "x" * 501  # Exceeds max_length of 500

        project = Project(
            title="Test",
            description="Test description",
            technologies=long_tech
        )

        with pytest.raises(ValidationError):
            project.full_clean()

    def test_project_url_validation(self):
        """Test that url field validates URL format."""
        project = Project(
            title="Test",
            description="Test description",
            url="not-a-valid-url"
        )

        with pytest.raises(ValidationError):
            project.full_clean()

    def test_project_github_url_validation(self):
        """Test that github_url field validates URL format."""
        project = Project(
            title="Test",
            description="Test description",
            github_url="invalid-github-url"
        )

        with pytest.raises(ValidationError):
            project.full_clean()

    def test_project_created_at_auto_set(self):
        """Test that created_at is automatically set on creation."""
        before = timezone.now()
        project = Project.objects.create(
            title="Timestamp Test",
            description="Testing timestamps"
        )
        after = timezone.now()

        assert before <= project.created_at <= after

    def test_project_updated_at_auto_updates(self):
        """Test that updated_at is automatically updated on save."""
        project = Project.objects.create(
            title="Update Test",
            description="Testing update timestamp"
        )

        original_updated = project.updated_at

        # Wait a tiny bit to ensure timestamp difference
        import time
        time.sleep(0.01)

        project.title = "Updated Title"
        project.save()

        assert project.updated_at > original_updated

    def test_project_is_featured_default_false(self):
        """Test that is_featured defaults to False."""
        project = Project.objects.create(
            title="Featured Test",
            description="Testing featured default"
        )

        assert project.is_featured is False

    def test_project_order_default_zero(self):
        """Test that order defaults to 0."""
        project = Project.objects.create(
            title="Order Test",
            description="Testing order default"
        )

        assert project.order == 0

    def test_project_blank_fields_allowed(self):
        """Test that blank=True fields can be empty strings."""
        project = Project.objects.create(
            title="Blank Fields Test",
            description="Testing blank fields",
            short_description="",
            url="",
            github_url="",
            technologies="",
            phone=""
        )

        project.full_clean()  # Should not raise validation error
        assert project.short_description == ""
        assert project.url == ""
        assert project.github_url == ""
        assert project.technologies == ""

    def test_project_description_required(self):
        """Test that description field is required."""
        project = Project(
            title="Missing Description",
            description=""
        )

        with pytest.raises(ValidationError):
            project.full_clean()

    def test_multiple_projects_can_be_featured(self):
        """Test that multiple projects can be marked as featured."""
        project1 = Project.objects.create(
            title="Featured 1",
            description="First featured project",
            is_featured=True
        )
        project2 = Project.objects.create(
            title="Featured 2",
            description="Second featured project",
            is_featured=True
        )

        featured_count = Project.objects.filter(is_featured=True).count()
        assert featured_count == 2

    def test_project_meta_verbose_names(self):
        """Test the Meta class verbose names."""
        assert Project._meta.verbose_name == "Project"
        assert Project._meta.verbose_name_plural == "Projects"

    def test_project_filtering_by_featured(self):
        """Test filtering projects by is_featured flag."""
        Project.objects.create(
            title="Regular Project",
            description="Not featured",
            is_featured=False
        )
        Project.objects.create(
            title="Featured Project",
            description="This is featured",
            is_featured=True
        )

        featured_projects = Project.objects.filter(is_featured=True)
        assert featured_projects.count() == 1
        assert featured_projects.first().title == "Featured Project"
