"""
Tests for AboutMe model.
"""

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.about.models import AboutMe


@pytest.mark.django_db
class TestAboutMeModel:
    """Test suite for AboutMe model."""

    def test_create_about_me_with_required_fields(self):
        """Test creating an AboutMe profile with only required fields."""
        about = AboutMe.objects.create(
            name="John Doe",
            title="Software Engineer",
            bio="Passionate software engineer with 5 years of experience.",
            email="john@example.com"
        )

        assert about.id is not None
        assert about.name == "John Doe"
        assert about.title == "Software Engineer"
        assert about.bio == "Passionate software engineer with 5 years of experience."
        assert about.email == "john@example.com"
        assert about.phone == ""
        assert about.location == ""
        assert about.linkedin_url == ""
        assert about.github_url == ""
        assert about.twitter_url == ""
        assert about.website_url == ""
        assert about.is_active is True
        assert about.created_at is not None
        assert about.updated_at is not None

    def test_create_about_me_with_all_fields(self):
        """Test creating an AboutMe profile with all fields populated."""
        about = AboutMe.objects.create(
            name="Jane Smith",
            title="Full Stack Developer",
            bio="Experienced full-stack developer specializing in Python and React.",
            email="jane@example.com",
            phone="+1234567890",
            location="San Francisco, CA",
            linkedin_url="https://linkedin.com/in/janesmith",
            github_url="https://github.com/janesmith",
            twitter_url="https://twitter.com/janesmith",
            website_url="https://janesmith.dev",
            is_active=True
        )

        assert about.name == "Jane Smith"
        assert about.phone == "+1234567890"
        assert about.location == "San Francisco, CA"
        assert about.linkedin_url == "https://linkedin.com/in/janesmith"
        assert about.github_url == "https://github.com/janesmith"
        assert about.twitter_url == "https://twitter.com/janesmith"
        assert about.website_url == "https://janesmith.dev"

    def test_about_me_str_representation(self):
        """Test the string representation of an AboutMe profile."""
        about = AboutMe.objects.create(
            name="Alice Johnson",
            title="Data Scientist",
            bio="Data scientist with ML expertise.",
            email="alice@example.com"
        )

        assert str(about) == "Alice Johnson"

    def test_about_me_ordering_default(self):
        """Test that AboutMe profiles are ordered by created_at descending."""
        about1 = AboutMe.objects.create(
            name="First Person",
            title="Developer",
            bio="First profile",
            email="first@example.com"
        )
        about2 = AboutMe.objects.create(
            name="Second Person",
            title="Engineer",
            bio="Second profile",
            email="second@example.com"
        )

        profiles = list(AboutMe.objects.all())

        # Most recent first
        assert profiles[0] == about2
        assert profiles[1] == about1

    def test_only_one_active_profile(self):
        """Test that setting a profile as active deactivates all others."""
        about1 = AboutMe.objects.create(
            name="Profile 1",
            title="Developer",
            bio="First profile",
            email="profile1@example.com",
            is_active=True
        )

        about2 = AboutMe.objects.create(
            name="Profile 2",
            title="Engineer",
            bio="Second profile",
            email="profile2@example.com",
            is_active=True  # This should deactivate about1
        )

        # Refresh from database
        about1.refresh_from_db()

        assert about1.is_active is False
        assert about2.is_active is True

    def test_multiple_inactive_profiles_allowed(self):
        """Test that multiple inactive profiles can coexist."""
        about1 = AboutMe.objects.create(
            name="Inactive 1",
            title="Developer",
            bio="First inactive",
            email="inactive1@example.com",
            is_active=False
        )
        about2 = AboutMe.objects.create(
            name="Inactive 2",
            title="Engineer",
            bio="Second inactive",
            email="inactive2@example.com",
            is_active=False
        )

        assert about1.is_active is False
        assert about2.is_active is False
        assert AboutMe.objects.filter(is_active=False).count() == 2

    def test_activating_inactive_profile(self):
        """Test activating a previously inactive profile."""
        about1 = AboutMe.objects.create(
            name="Active Profile",
            title="Developer",
            bio="Active",
            email="active@example.com",
            is_active=True
        )

        about2 = AboutMe.objects.create(
            name="Inactive Profile",
            title="Engineer",
            bio="Inactive",
            email="inactive@example.com",
            is_active=False
        )

        # Now activate about2
        about2.is_active = True
        about2.save()

        about1.refresh_from_db()

        assert about1.is_active is False
        assert about2.is_active is True

    def test_name_max_length(self):
        """Test that name field respects max_length constraint."""
        long_name = "x" * 201  # Exceeds max_length of 200

        about = AboutMe(
            name=long_name,
            title="Developer",
            bio="Bio text",
            email="test@example.com"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_title_max_length(self):
        """Test that title field respects max_length constraint."""
        long_title = "x" * 201  # Exceeds max_length of 200

        about = AboutMe(
            name="Test Name",
            title=long_title,
            bio="Bio text",
            email="test@example.com"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_phone_max_length(self):
        """Test that phone field respects max_length constraint."""
        long_phone = "1" * 21  # Exceeds max_length of 20

        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="test@example.com",
            phone=long_phone
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_location_max_length(self):
        """Test that location field respects max_length constraint."""
        long_location = "x" * 201  # Exceeds max_length of 200

        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="test@example.com",
            location=long_location
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_email_validation(self):
        """Test that email field validates email format."""
        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="not-a-valid-email"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_linkedin_url_validation(self):
        """Test that linkedin_url field validates URL format."""
        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="test@example.com",
            linkedin_url="not-a-valid-url"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_github_url_validation(self):
        """Test that github_url field validates URL format."""
        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="test@example.com",
            github_url="invalid-github-url"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_twitter_url_validation(self):
        """Test that twitter_url field validates URL format."""
        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="test@example.com",
            twitter_url="not-a-url"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_website_url_validation(self):
        """Test that website_url field validates URL format."""
        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="Bio text",
            email="test@example.com",
            website_url="invalid-website"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_created_at_auto_set(self):
        """Test that created_at is automatically set on creation."""
        before = timezone.now()
        about = AboutMe.objects.create(
            name="Timestamp Test",
            title="Developer",
            bio="Testing timestamps",
            email="timestamp@example.com"
        )
        after = timezone.now()

        assert before <= about.created_at <= after

    def test_updated_at_auto_updates(self):
        """Test that updated_at is automatically updated on save."""
        about = AboutMe.objects.create(
            name="Update Test",
            title="Developer",
            bio="Testing update timestamp",
            email="update@example.com"
        )

        original_updated = about.updated_at

        # Wait a tiny bit to ensure timestamp difference
        import time
        time.sleep(0.01)

        about.name = "Updated Name"
        about.save()

        assert about.updated_at > original_updated

    def test_is_active_default_true(self):
        """Test that is_active defaults to True."""
        about = AboutMe.objects.create(
            name="Active Default Test",
            title="Developer",
            bio="Testing active default",
            email="active@example.com"
        )

        assert about.is_active is True

    def test_blank_optional_fields(self):
        """Test that optional fields can be blank."""
        about = AboutMe.objects.create(
            name="Minimal Profile",
            title="Developer",
            bio="Minimal bio",
            email="minimal@example.com",
            phone="",
            location="",
            linkedin_url="",
            github_url="",
            twitter_url="",
            website_url=""
        )

        about.full_clean()  # Should not raise validation error
        assert about.phone == ""
        assert about.location == ""

    def test_required_fields_validation(self):
        """Test that required fields cannot be empty."""
        about = AboutMe(
            name="",
            title="Developer",
            bio="Bio",
            email="test@example.com"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_bio_required(self):
        """Test that bio field is required."""
        about = AboutMe(
            name="Test Name",
            title="Developer",
            bio="",
            email="test@example.com"
        )

        with pytest.raises(ValidationError):
            about.full_clean()

    def test_meta_verbose_names(self):
        """Test the Meta class verbose names."""
        assert AboutMe._meta.verbose_name == "About Me"
        assert AboutMe._meta.verbose_name_plural == "About Me"

    def test_get_active_profile(self):
        """Test retrieving the active profile."""
        AboutMe.objects.create(
            name="Inactive",
            title="Developer",
            bio="Inactive profile",
            email="inactive@example.com",
            is_active=False
        )
        active = AboutMe.objects.create(
            name="Active",
            title="Engineer",
            bio="Active profile",
            email="active@example.com",
            is_active=True
        )

        active_profile = AboutMe.objects.filter(is_active=True).first()
        assert active_profile == active

    def test_save_override_ensures_single_active(self):
        """Test that the custom save method ensures only one active profile."""
        about1 = AboutMe.objects.create(
            name="First Active",
            title="Developer",
            bio="First",
            email="first@example.com",
            is_active=True
        )

        about2 = AboutMe.objects.create(
            name="Second Active",
            title="Engineer",
            bio="Second",
            email="second@example.com",
            is_active=True
        )

        about3 = AboutMe.objects.create(
            name="Third Active",
            title="Designer",
            bio="Third",
            email="third@example.com",
            is_active=True
        )

        # Only the last one should be active
        assert AboutMe.objects.filter(is_active=True).count() == 1
        assert AboutMe.objects.get(is_active=True) == about3

    def test_update_active_profile_keeps_single_active(self):
        """Test that updating active status maintains single active profile."""
        about1 = AboutMe.objects.create(
            name="Profile 1",
            title="Developer",
            bio="First",
            email="first@example.com",
            is_active=True
        )

        about2 = AboutMe.objects.create(
            name="Profile 2",
            title="Engineer",
            bio="Second",
            email="second@example.com",
            is_active=False
        )

        # Activate profile 2
        about2.is_active = True
        about2.save()

        about1.refresh_from_db()

        assert about1.is_active is False
        assert about2.is_active is True
        assert AboutMe.objects.filter(is_active=True).count() == 1
