"""
Tests for ContactMessage model.
"""

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.contact.models import ContactMessage


@pytest.mark.django_db
class TestContactMessageModel:
    """Test suite for ContactMessage model."""

    def test_create_contact_message_with_required_fields(self):
        """Test creating a contact message with only required fields."""
        message = ContactMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="This is a test message."
        )

        assert message.id is not None
        assert message.name == "John Doe"
        assert message.email == "john@example.com"
        assert message.subject == "Test Subject"
        assert message.message == "This is a test message."
        assert message.phone == ""
        assert message.is_read is False
        assert message.is_replied is False
        assert message.created_at is not None
        assert message.updated_at is not None

    def test_create_contact_message_with_all_fields(self):
        """Test creating a contact message with all fields populated."""
        message = ContactMessage.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            subject="Inquiry about services",
            message="I would like to know more about your services.",
            phone="+1234567890",
            is_read=True,
            is_replied=True
        )

        assert message.name == "Jane Smith"
        assert message.email == "jane@example.com"
        assert message.subject == "Inquiry about services"
        assert message.message == "I would like to know more about your services."
        assert message.phone == "+1234567890"
        assert message.is_read is True
        assert message.is_replied is True

    def test_contact_message_str_representation(self):
        """Test the string representation of a contact message."""
        message = ContactMessage.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            subject="Website Feedback",
            message="Great website!"
        )

        assert str(message) == "Alice Johnson - Website Feedback"

    def test_contact_message_ordering_default(self):
        """Test that contact messages are ordered by created_at descending."""
        message1 = ContactMessage.objects.create(
            name="First Person",
            email="first@example.com",
            subject="First Subject",
            message="First message"
        )
        message2 = ContactMessage.objects.create(
            name="Second Person",
            email="second@example.com",
            subject="Second Subject",
            message="Second message"
        )

        messages = list(ContactMessage.objects.all())

        # Most recent first
        assert messages[0] == message2
        assert messages[1] == message1

    def test_name_max_length(self):
        """Test that name field respects max_length constraint."""
        long_name = "x" * 201  # Exceeds max_length of 200

        message = ContactMessage(
            name=long_name,
            email="test@example.com",
            subject="Subject",
            message="Message"
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_subject_max_length(self):
        """Test that subject field respects max_length constraint."""
        long_subject = "x" * 301  # Exceeds max_length of 300

        message = ContactMessage(
            name="Test Name",
            email="test@example.com",
            subject=long_subject,
            message="Message"
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_phone_max_length(self):
        """Test that phone field respects max_length constraint."""
        long_phone = "1" * 21  # Exceeds max_length of 20

        message = ContactMessage(
            name="Test Name",
            email="test@example.com",
            subject="Subject",
            message="Message",
            phone=long_phone
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_email_validation(self):
        """Test that email field validates email format."""
        message = ContactMessage(
            name="Test Name",
            email="not-a-valid-email",
            subject="Subject",
            message="Message"
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_created_at_auto_set(self):
        """Test that created_at is automatically set on creation."""
        before = timezone.now()
        message = ContactMessage.objects.create(
            name="Timestamp Test",
            email="timestamp@example.com",
            subject="Testing timestamps",
            message="Test message"
        )
        after = timezone.now()

        assert before <= message.created_at <= after

    def test_updated_at_auto_updates(self):
        """Test that updated_at is automatically updated on save."""
        message = ContactMessage.objects.create(
            name="Update Test",
            email="update@example.com",
            subject="Testing update timestamp",
            message="Test message"
        )

        original_updated = message.updated_at

        # Wait a tiny bit to ensure timestamp difference
        import time
        time.sleep(0.01)

        message.subject = "Updated Subject"
        message.save()

        assert message.updated_at > original_updated

    def test_is_read_default_false(self):
        """Test that is_read defaults to False."""
        message = ContactMessage.objects.create(
            name="Read Test",
            email="read@example.com",
            subject="Testing read default",
            message="Test message"
        )

        assert message.is_read is False

    def test_is_replied_default_false(self):
        """Test that is_replied defaults to False."""
        message = ContactMessage.objects.create(
            name="Replied Test",
            email="replied@example.com",
            subject="Testing replied default",
            message="Test message"
        )

        assert message.is_replied is False

    def test_mark_as_read(self):
        """Test marking a message as read."""
        message = ContactMessage.objects.create(
            name="Mark Read",
            email="markread@example.com",
            subject="Subject",
            message="Message"
        )

        assert message.is_read is False

        message.is_read = True
        message.save()

        assert message.is_read is True

    def test_mark_as_replied(self):
        """Test marking a message as replied."""
        message = ContactMessage.objects.create(
            name="Mark Replied",
            email="markreplied@example.com",
            subject="Subject",
            message="Message"
        )

        assert message.is_replied is False

        message.is_replied = True
        message.save()

        assert message.is_replied is True

    def test_phone_optional(self):
        """Test that phone field is optional."""
        message = ContactMessage.objects.create(
            name="No Phone",
            email="nophone@example.com",
            subject="Subject",
            message="Message without phone"
        )

        message.full_clean()  # Should not raise validation error
        assert message.phone == ""

    def test_required_fields_validation(self):
        """Test that required fields cannot be empty."""
        message = ContactMessage(
            name="",
            email="test@example.com",
            subject="Subject",
            message="Message"
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_message_text_required(self):
        """Test that message field is required."""
        message = ContactMessage(
            name="Test Name",
            email="test@example.com",
            subject="Subject",
            message=""
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_subject_required(self):
        """Test that subject field is required."""
        message = ContactMessage(
            name="Test Name",
            email="test@example.com",
            subject="",
            message="Message"
        )

        with pytest.raises(ValidationError):
            message.full_clean()

    def test_meta_verbose_names(self):
        """Test the Meta class verbose names."""
        assert ContactMessage._meta.verbose_name == "Contact Message"
        assert ContactMessage._meta.verbose_name_plural == "Contact Messages"

    def test_filter_unread_messages(self):
        """Test filtering messages by is_read status."""
        ContactMessage.objects.create(
            name="Read Message",
            email="read@example.com",
            subject="Subject",
            message="Message",
            is_read=True
        )
        ContactMessage.objects.create(
            name="Unread Message",
            email="unread@example.com",
            subject="Subject",
            message="Message",
            is_read=False
        )

        unread_messages = ContactMessage.objects.filter(is_read=False)
        assert unread_messages.count() == 1
        assert unread_messages.first().name == "Unread Message"

    def test_filter_replied_messages(self):
        """Test filtering messages by is_replied status."""
        ContactMessage.objects.create(
            name="Replied Message",
            email="replied@example.com",
            subject="Subject",
            message="Message",
            is_replied=True
        )
        ContactMessage.objects.create(
            name="Not Replied Message",
            email="notreplied@example.com",
            subject="Subject",
            message="Message",
            is_replied=False
        )

        replied_messages = ContactMessage.objects.filter(is_replied=True)
        assert replied_messages.count() == 1
        assert replied_messages.first().name == "Replied Message"

    def test_long_message_text(self):
        """Test that TextField can hold long messages."""
        long_message = "x" * 5000

        message = ContactMessage.objects.create(
            name="Long Message",
            email="long@example.com",
            subject="Long message test",
            message=long_message
        )

        assert len(message.message) == 5000

    def test_email_with_special_characters(self):
        """Test that email field accepts valid emails with special characters."""
        message = ContactMessage.objects.create(
            name="Special Email",
            email="user.name+tag@example.co.uk",
            subject="Subject",
            message="Message"
        )

        message.full_clean()  # Should not raise validation error
        assert message.email == "user.name+tag@example.co.uk"

    def test_phone_with_formatting(self):
        """Test that phone field accepts various phone formats."""
        message = ContactMessage.objects.create(
            name="Phone Format",
            email="phone@example.com",
            subject="Subject",
            message="Message",
            phone="+1 (555) 123-4567"
        )

        assert message.phone == "+1 (555) 123-4567"

    def test_multiple_unread_messages(self):
        """Test creating multiple unread messages."""
        ContactMessage.objects.create(
            name="Unread 1",
            email="unread1@example.com",
            subject="Subject 1",
            message="Message 1",
            is_read=False
        )
        ContactMessage.objects.create(
            name="Unread 2",
            email="unread2@example.com",
            subject="Subject 2",
            message="Message 2",
            is_read=False
        )

        unread_count = ContactMessage.objects.filter(is_read=False).count()
        assert unread_count == 2

    def test_mark_read_and_replied_together(self):
        """Test marking a message as both read and replied."""
        message = ContactMessage.objects.create(
            name="Read and Replied",
            email="both@example.com",
            subject="Subject",
            message="Message"
        )

        message.is_read = True
        message.is_replied = True
        message.save()

        assert message.is_read is True
        assert message.is_replied is True

    def test_message_with_unicode_characters(self):
        """Test that message field handles unicode characters."""
        message = ContactMessage.objects.create(
            name="Unicode Test",
            email="unicode@example.com",
            subject="Test Subject",
            message="Hello! This message contains unicode: 你好, مرحبا, Привет"
        )

        assert "你好" in message.message
        assert "مرحبا" in message.message
        assert "Привет" in message.message
