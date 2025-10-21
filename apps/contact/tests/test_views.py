"""
Tests for ContactMessage API views.
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.contact.models import ContactMessage


@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()


@pytest.fixture
def sample_message():
    """Fixture for creating a sample contact message."""
    return ContactMessage.objects.create(
        name='John Doe',
        email='john@example.com',
        subject='Inquiry',
        message='I have a question about your services.',
        phone='+1234567890',
        is_read=False,
        is_replied=False
    )


@pytest.fixture
def read_message():
    """Fixture for creating a read message."""
    return ContactMessage.objects.create(
        name='Jane Smith',
        email='jane@example.com',
        subject='Follow-up',
        message='Following up on my previous inquiry.',
        is_read=True,
        is_replied=False
    )


@pytest.fixture
def replied_message():
    """Fixture for creating a replied message."""
    return ContactMessage.objects.create(
        name='Bob Johnson',
        email='bob@example.com',
        subject='Thanks',
        message='Thank you for your response.',
        is_read=True,
        is_replied=True
    )


@pytest.mark.django_db
class TestContactMessageViewSet:
    """Test suite for ContactMessageViewSet."""

    def test_list_contact_messages(self, api_client, sample_message):
        """Test retrieving list of all contact messages."""
        url = '/api/contact/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'John Doe'

    def test_list_contact_messages_empty(self, api_client):
        """Test retrieving empty list when no messages exist."""
        url = '/api/contact/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_list_multiple_messages(self, api_client, sample_message, read_message):
        """Test retrieving list with multiple messages."""
        url = '/api/contact/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_contact_message(self, api_client, sample_message):
        """Test retrieving a single contact message by ID."""
        url = f'/api/contact/{sample_message.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_message.id
        assert response.data['name'] == 'John Doe'
        assert response.data['email'] == 'john@example.com'
        assert response.data['subject'] == 'Inquiry'

    def test_retrieve_nonexistent_message(self, api_client):
        """Test retrieving a message that doesn't exist."""
        url = '/api/contact/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_contact_message(self, api_client):
        """Test creating a new contact message (public endpoint)."""
        url = '/api/contact/'
        data = {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'subject': 'New Inquiry',
            'message': 'I would like to inquire about your services.',
            'phone': '+1987654321'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Alice Johnson'
        assert response.data['email'] == 'alice@example.com'
        assert response.data['subject'] == 'New Inquiry'
        assert ContactMessage.objects.count() == 1

    def test_create_message_minimal_data(self, api_client):
        """Test creating a message with only required fields."""
        url = '/api/contact/'
        data = {
            'name': 'Minimal User',
            'email': 'minimal@example.com',
            'subject': 'Minimal Subject',
            'message': 'Minimal message'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Minimal User'

    def test_create_message_missing_required_name(self, api_client):
        """Test creating a message without required name field."""
        url = '/api/contact/'
        data = {
            'email': 'test@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_create_message_missing_required_email(self, api_client):
        """Test creating a message without required email field."""
        url = '/api/contact/'
        data = {
            'name': 'Test Name',
            'subject': 'Subject',
            'message': 'Message'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_create_message_invalid_email(self, api_client):
        """Test creating a message with invalid email."""
        url = '/api/contact/'
        data = {
            'name': 'Test Name',
            'email': 'not-a-valid-email',
            'subject': 'Subject',
            'message': 'Message'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_update_message_full(self, api_client, sample_message):
        """Test full update of a message (PUT)."""
        url = f'/api/contact/{sample_message.id}/'
        data = {
            'name': 'John Updated',
            'email': 'johnupdated@example.com',
            'subject': 'Updated Subject',
            'message': 'Updated message content.',
            'phone': '+1111111111',
            'isRead': True,
            'isReplied': True
        }

        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'John Updated'
        assert response.data['isRead'] is True
        assert response.data['isReplied'] is True

    def test_partial_update_message(self, api_client, sample_message):
        """Test partial update of a message (PATCH)."""
        url = f'/api/contact/{sample_message.id}/'
        data = {
            'isRead': True
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isRead'] is True
        assert response.data['name'] == 'John Doe'  # Unchanged

    def test_delete_message(self, api_client, sample_message):
        """Test deleting a message."""
        message_id = sample_message.id
        url = f'/api/contact/{message_id}/'

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ContactMessage.objects.filter(id=message_id).exists()

    def test_mark_read_action(self, api_client, sample_message):
        """Test the mark_read custom action."""
        url = f'/api/contact/{sample_message.id}/mark_read/'
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isRead'] is True

        # Verify in database
        sample_message.refresh_from_db()
        assert sample_message.is_read is True

    def test_mark_replied_action(self, api_client, sample_message):
        """Test the mark_replied custom action."""
        url = f'/api/contact/{sample_message.id}/mark_replied/'
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isReplied'] is True

        # Verify in database
        sample_message.refresh_from_db()
        assert sample_message.is_replied is True

    def test_unread_messages_action(self, api_client, sample_message, read_message):
        """Test the unread custom action to retrieve unread messages."""
        url = '/api/contact/unread/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == sample_message.id
        assert response.data[0]['isRead'] is False

    def test_unread_messages_action_empty(self, api_client, read_message):
        """Test unread action when all messages are read."""
        url = '/api/contact/unread/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_unread_messages_action_no_messages(self, api_client):
        """Test unread action when no messages exist."""
        url = '/api/contact/unread/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_response_field_names_camelcase(self, api_client, sample_message):
        """Test that API responses use camelCase field names."""
        url = f'/api/contact/{sample_message.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'isRead' in response.data
        assert 'isReplied' in response.data
        assert 'createdAt' in response.data
        assert 'updatedAt' in response.data

    def test_list_ordering_by_created_at_desc(self, api_client):
        """Test that messages are ordered by created_at descending."""
        message1 = ContactMessage.objects.create(
            name='First',
            email='first@example.com',
            subject='First Subject',
            message='First message'
        )
        message2 = ContactMessage.objects.create(
            name='Second',
            email='second@example.com',
            subject='Second Subject',
            message='Second message'
        )

        url = '/api/contact/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Most recent first
        assert response.data[0]['name'] == 'Second'
        assert response.data[1]['name'] == 'First'

    def test_api_content_type_json(self, api_client, sample_message):
        """Test that API responses have JSON content type."""
        url = f'/api/contact/{sample_message.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']

    def test_create_message_uses_create_serializer(self, api_client):
        """Test that create action uses ContactMessageCreateSerializer."""
        url = '/api/contact/'
        data = {
            'name': 'Create Test',
            'email': 'create@example.com',
            'subject': 'Subject',
            'message': 'Message'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        # Verify that isRead and isReplied are set to default False
        created_message = ContactMessage.objects.get(id=response.data['id'])
        assert created_message.is_read is False
        assert created_message.is_replied is False

    def test_mark_read_already_read_message(self, api_client, read_message):
        """Test marking an already read message as read."""
        url = f'/api/contact/{read_message.id}/mark_read/'
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isRead'] is True

    def test_mark_replied_already_replied_message(self, api_client, replied_message):
        """Test marking an already replied message as replied."""
        url = f'/api/contact/{replied_message.id}/mark_replied/'
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isReplied'] is True

    def test_multiple_unread_messages(self, api_client):
        """Test retrieving multiple unread messages."""
        ContactMessage.objects.create(
            name='Unread 1',
            email='unread1@example.com',
            subject='Subject 1',
            message='Message 1',
            is_read=False
        )
        ContactMessage.objects.create(
            name='Unread 2',
            email='unread2@example.com',
            subject='Subject 2',
            message='Message 2',
            is_read=False
        )
        ContactMessage.objects.create(
            name='Read',
            email='read@example.com',
            subject='Subject',
            message='Message',
            is_read=True
        )

        url = '/api/contact/unread/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_message_with_phone(self, api_client):
        """Test creating a message with phone number."""
        url = '/api/contact/'
        data = {
            'name': 'Phone Test',
            'email': 'phone@example.com',
            'subject': 'Phone Subject',
            'message': 'Message with phone',
            'phone': '+1 (555) 123-4567'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['phone'] == '+1 (555) 123-4567'

    def test_create_message_without_phone(self, api_client):
        """Test creating a message without phone number."""
        url = '/api/contact/'
        data = {
            'name': 'No Phone',
            'email': 'nophone@example.com',
            'subject': 'No Phone Subject',
            'message': 'Message without phone'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['phone'] == ''

    def test_message_not_found_returns_404(self, api_client):
        """Test that requesting non-existent message returns 404."""
        url = '/api/contact/99999/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_mark_read_nonexistent_message(self, api_client):
        """Test marking a non-existent message as read."""
        url = '/api/contact/99999/mark_read/'
        response = api_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_mark_replied_nonexistent_message(self, api_client):
        """Test marking a non-existent message as replied."""
        url = '/api/contact/99999/mark_replied/'
        response = api_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_message_read_and_replied_together(self, api_client, sample_message):
        """Test updating both read and replied status together."""
        url = f'/api/contact/{sample_message.id}/'
        data = {
            'isRead': True,
            'isReplied': True
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['isRead'] is True
        assert response.data['isReplied'] is True

    def test_filter_by_status_combinations(self, api_client, sample_message, read_message, replied_message):
        """Test that messages with different status combinations are handled correctly."""
        url = '/api/contact/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        # Verify different statuses
        statuses = [(msg['isRead'], msg['isReplied']) for msg in response.data]
        assert (False, False) in statuses  # sample_message
        assert (True, False) in statuses   # read_message
        assert (True, True) in statuses    # replied_message

    def test_create_message_long_text(self, api_client):
        """Test creating a message with long text content."""
        long_message = "x" * 1000

        url = '/api/contact/'
        data = {
            'name': 'Long Message',
            'email': 'long@example.com',
            'subject': 'Long Message Test',
            'message': long_message
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data['message']) == 1000
