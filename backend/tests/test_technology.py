import pytest
from rest_framework import status
from .conftest import TechnologiesFactory


@pytest.mark.django_db
class TestTechnologiesViewSet:
    BASE_URL = "/api/technologies/"

    def test_list_technologies(self, api_client):
        TechnologiesFactory.create_batch(3)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_technology(self, api_client):
        data = {"name": "Python", "icon": "devicon-python-plain", "color": "#3776ab"}
        response = api_client.post(self.BASE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Python"
        assert response.data["color"] == "#3776ab"

    def test_retrieve_technology(self, api_client):
        tech = TechnologiesFactory()
        response = api_client.get(f"{self.BASE_URL}{tech.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == tech.name

    def test_update_technology(self, api_client):
        tech = TechnologiesFactory()
        response = api_client.patch(f"{self.BASE_URL}{tech.id}/", {"name": "Updated"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated"

    def test_delete_technology(self, api_client):
        tech = TechnologiesFactory()
        response = api_client.delete(f"{self.BASE_URL}{tech.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_technology_str(self):
        tech = TechnologiesFactory.build(name="Django")
        assert str(tech) == "Django"
