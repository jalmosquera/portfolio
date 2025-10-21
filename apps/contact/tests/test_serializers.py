"""
Tests for ContactMessage serializers.
"""

import pytest
from apps.contact.models import ContactMessage
from apps.contact.api.serializers import (
    ContactMessageSerializer,
    ContactMessageCreateSerializer
)


@pytest.mark.django_db
class TestContactMessageSerializer:
    """Test suite for ContactMessageSerializer."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid data."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Inquiry',
            'message': 'I have a question about your services.',
            'phone': '+1234567890',
            'isRead': False,
            'isReplied': False
        }

        serializer = ContactMessageSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.name == 'John Doe'
        assert contact_message.email == 'john@example.com'
        assert contact_message.subject == 'Inquiry'
        assert contact_message.message == 'I have a question about your services.'
        assert contact_message.phone == '+1234567890'
        assert contact_message.is_read is False
        assert contact_message.is_replied is False

    def test_serializer_with_minimal_data(self):
        """Test serializer with only required fields."""
        data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'subject': 'Hello',
            'message': 'Hello there!'
        }

        serializer = ContactMessageSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.name == 'Jane Smith'
        assert contact_message.email == 'jane@example.com'
        assert contact_message.phone == ''
        assert contact_message.is_read is False

    def test_serializer_missing_required_name(self):
        """Test serializer validation fails when name is missing."""
        data = {
            'email': 'test@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_serializer_missing_required_email(self):
        """Test serializer validation fails when email is missing."""
        data = {
            'name': 'Test Name',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_serializer_missing_required_subject(self):
        """Test serializer validation fails when subject is missing."""
        data = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'message': 'Message'
        }

        serializer = ContactMessageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'subject' in serializer.errors

    def test_serializer_missing_required_message(self):
        """Test serializer validation fails when message is missing."""
        data = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'subject': 'Subject'
        }

        serializer = ContactMessageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'message' in serializer.errors

    def test_serializer_camelcase_field_mapping(self):
        """Test that camelCase fields map correctly to snake_case."""
        contact_message = ContactMessage.objects.create(
            name='Camel Case Test',
            email='camel@example.com',
            subject='Test Subject',
            message='Test message',
            is_read=True,
            is_replied=True
        )

        serializer = ContactMessageSerializer(contact_message)

        assert 'isRead' in serializer.data
        assert 'isReplied' in serializer.data
        assert 'createdAt' in serializer.data
        assert 'updatedAt' in serializer.data

        assert serializer.data['isRead'] is True
        assert serializer.data['isReplied'] is True

    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be modified via serializer."""
        contact_message = ContactMessage.objects.create(
            name='Read-only Test',
            email='readonly@example.com',
            subject='Subject',
            message='Message'
        )

        original_id = contact_message.id
        original_created = contact_message.created_at

        data = {
            'id': 99999,
            'name': 'Updated Name',
            'email': 'updated@example.com',
            'subject': 'Updated Subject',
            'message': 'Updated message',
            'createdAt': '2020-01-01T00:00:00Z',
            'updatedAt': '2020-01-01T00:00:00Z'
        }

        serializer = ContactMessageSerializer(contact_message, data=data)
        assert serializer.is_valid()
        updated_message = serializer.save()

        # ID and createdAt should not change
        assert updated_message.id == original_id
        assert updated_message.created_at == original_created
        # Other fields should update
        assert updated_message.name == 'Updated Name'

    def test_serializer_email_validation(self):
        """Test that email field is validated."""
        data = {
            'name': 'Email Test',
            'email': 'not-a-valid-email',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_serializer_boolean_field_defaults(self):
        """Test that boolean fields have correct default values."""
        data = {
            'name': 'Boolean Test',
            'email': 'boolean@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.is_read is False
        assert contact_message.is_replied is False

    def test_serializer_output_structure(self):
        """Test that serializer output has all expected fields."""
        contact_message = ContactMessage.objects.create(
            name='Structure Test',
            email='structure@example.com',
            subject='Subject',
            message='Message'
        )

        serializer = ContactMessageSerializer(contact_message)
        expected_fields = {
            'id', 'name', 'email', 'subject', 'message', 'phone',
            'isRead', 'isReplied', 'createdAt', 'updatedAt'
        }

        assert set(serializer.data.keys()) == expected_fields

    def test_serializer_update_partial(self):
        """Test partial update of a contact message."""
        contact_message = ContactMessage.objects.create(
            name='Original Name',
            email='original@example.com',
            subject='Original Subject',
            message='Original message',
            is_read=False
        )

        data = {'isRead': True}

        serializer = ContactMessageSerializer(contact_message, data=data, partial=True)
        assert serializer.is_valid()
        updated_message = serializer.save()

        assert updated_message.is_read is True
        assert updated_message.name == 'Original Name'
        assert updated_message.subject == 'Original Subject'

    def test_serializer_phone_optional(self):
        """Test that phone field is optional."""
        data = {
            'name': 'No Phone',
            'email': 'nophone@example.com',
            'subject': 'Subject',
            'message': 'Message',
            'phone': ''
        }

        serializer = ContactMessageSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_list_serialization(self):
        """Test serializing multiple contact messages."""
        ContactMessage.objects.create(
            name='Message 1',
            email='message1@example.com',
            subject='Subject 1',
            message='First message'
        )
        ContactMessage.objects.create(
            name='Message 2',
            email='message2@example.com',
            subject='Subject 2',
            message='Second message'
        )

        messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(messages, many=True)

        assert len(serializer.data) == 2

    def test_serializer_toggle_read_status(self):
        """Test toggling isRead field."""
        contact_message = ContactMessage.objects.create(
            name='Read Toggle',
            email='toggle@example.com',
            subject='Subject',
            message='Message',
            is_read=False
        )

        data = {'isRead': True}
        serializer = ContactMessageSerializer(contact_message, data=data, partial=True)
        assert serializer.is_valid()
        updated_message = serializer.save()

        assert updated_message.is_read is True

    def test_serializer_toggle_replied_status(self):
        """Test toggling isReplied field."""
        contact_message = ContactMessage.objects.create(
            name='Replied Toggle',
            email='replied@example.com',
            subject='Subject',
            message='Message',
            is_replied=False
        )

        data = {'isReplied': True}
        serializer = ContactMessageSerializer(contact_message, data=data, partial=True)
        assert serializer.is_valid()
        updated_message = serializer.save()

        assert updated_message.is_replied is True


@pytest.mark.django_db
class TestContactMessageCreateSerializer:
    """Test suite for ContactMessageCreateSerializer."""

    def test_create_serializer_with_valid_data(self):
        """Test create serializer with valid data."""
        data = {
            'name': 'Public User',
            'email': 'public@example.com',
            'subject': 'Public Inquiry',
            'message': 'This is a public inquiry.',
            'phone': '+1234567890'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.name == 'Public User'
        assert contact_message.email == 'public@example.com'
        assert contact_message.subject == 'Public Inquiry'
        assert contact_message.message == 'This is a public inquiry.'
        assert contact_message.phone == '+1234567890'

    def test_create_serializer_minimal_data(self):
        """Test create serializer with only required fields."""
        data = {
            'name': 'Minimal User',
            'email': 'minimal@example.com',
            'subject': 'Minimal Subject',
            'message': 'Minimal message'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.name == 'Minimal User'
        assert contact_message.phone == ''

    def test_create_serializer_fields_subset(self):
        """Test that create serializer only includes public fields."""
        data = {
            'name': 'Field Test',
            'email': 'field@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()

        # Create serializer should not have isRead or isReplied fields
        assert 'isRead' not in data
        assert 'isReplied' not in data

    def test_create_serializer_missing_required_field(self):
        """Test create serializer validation fails with missing field."""
        data = {
            'name': 'Test',
            'email': 'test@example.com',
            'subject': 'Subject'
            # Missing message
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'message' in serializer.errors

    def test_create_serializer_invalid_email(self):
        """Test create serializer validates email format."""
        data = {
            'name': 'Invalid Email',
            'email': 'invalid-email',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_create_serializer_sets_default_flags(self):
        """Test that create serializer sets default is_read and is_replied to False."""
        data = {
            'name': 'Default Flags',
            'email': 'flags@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.is_read is False
        assert contact_message.is_replied is False

    def test_create_serializer_does_not_expose_admin_fields(self):
        """Test that create serializer doesn't allow setting admin-only fields."""
        data = {
            'name': 'Admin Fields',
            'email': 'admin@example.com',
            'subject': 'Subject',
            'message': 'Message',
            'is_read': True,  # Should be ignored
            'is_replied': True  # Should be ignored
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        # These should remain False since they're not in the serializer fields
        assert contact_message.is_read is False
        assert contact_message.is_replied is False

    def test_create_serializer_output_fields(self):
        """Test the fields included in create serializer."""
        contact_message = ContactMessage.objects.create(
            name='Output Test',
            email='output@example.com',
            subject='Subject',
            message='Message'
        )

        serializer = ContactMessageCreateSerializer(contact_message)
        expected_fields = {'name', 'email', 'subject', 'message', 'phone'}

        assert set(serializer.data.keys()) == expected_fields

    def test_create_serializer_phone_optional(self):
        """Test that phone is optional in create serializer."""
        data = {
            'name': 'No Phone',
            'email': 'nophone@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.phone == ''

    def test_create_serializer_with_phone(self):
        """Test create serializer with phone number."""
        data = {
            'name': 'With Phone',
            'email': 'withphone@example.com',
            'subject': 'Subject',
            'message': 'Message',
            'phone': '+1 (555) 123-4567'
        }

        serializer = ContactMessageCreateSerializer(data=data)
        assert serializer.is_valid()
        contact_message = serializer.save()

        assert contact_message.phone == '+1 (555) 123-4567'
