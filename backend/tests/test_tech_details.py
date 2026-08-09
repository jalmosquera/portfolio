import pytest
from rest_framework import status
from .conftest import ProjectFactory, TechDetailFactory


@pytest.mark.django_db
class TestTechDetailViewSet:
    BASE_URL = "/api/tech-details/"

    def test_list_tech_details(self, api_client):
        TechDetailFactory.create_batch(3)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_filter_tech_details_by_project(self, api_client):
        project = ProjectFactory()
        expected = TechDetailFactory(project=project)
        TechDetailFactory()

        response = api_client.get(self.BASE_URL, {"project": project.id})

        assert response.status_code == status.HTTP_200_OK
        assert [detail["id"] for detail in response.data] == [expected.id]

    def test_create_tech_detail(self, api_client):
        project = ProjectFactory()
        data = {"project": project.id, "category": "Infrastructure", "text": "Docker"}
        response = api_client.post(self.BASE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["category"] == "Infrastructure"
        assert response.data["text"] == "Docker"

    def test_retrieve_tech_detail(self, api_client):
        detail = TechDetailFactory()
        response = api_client.get(f"{self.BASE_URL}{detail.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["category"] == detail.category

    def test_update_category(self, api_client):
        detail = TechDetailFactory()
        response = api_client.patch(f"{self.BASE_URL}{detail.id}/", {"category": "Frontend"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["category"] == "Frontend"

    def test_delete_tech_detail(self, api_client):
        detail = TechDetailFactory()
        response = api_client.delete(f"{self.BASE_URL}{detail.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_tech_details_related_name(self):
        project = ProjectFactory()
        TechDetailFactory.create_batch(2, project=project)
        assert project.tech_details.count() == 2
