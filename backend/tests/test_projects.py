import pytest
from rest_framework import status
from .conftest import ProjectFactory, TechnologiesFactory


@pytest.mark.django_db
class TestProjectsViewSet:
    BASE_URL = "/api/projects/"

    def test_list_projects(self, api_client):
        ProjectFactory.create_batch(3)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_project(self, api_client):
        data = {
            "title": "Alternativa 2.0",
            "slug": "alternativa-2-0",
            "short_description": "Restaurant SaaS Platform",
            "description": "Full description here.",
            "github": "https://github.com/example/alternativa",
            "live_url": "https://alternativa.app",
            "is_featured": True,
        }
        response = api_client.post(self.BASE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["slug"] == "alternativa-2-0"
        assert response.data["is_featured"] is True

    def test_retrieve_project(self, api_client):
        project = ProjectFactory()
        response = api_client.get(f"{self.BASE_URL}{project.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == project.title

    def test_update_project(self, api_client):
        project = ProjectFactory()
        response = api_client.patch(f"{self.BASE_URL}{project.id}/", {"title": "Updated Title"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"

    def test_delete_project(self, api_client):
        project = ProjectFactory()
        response = api_client.delete(f"{self.BASE_URL}{project.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_filter_is_featured(self, api_client):
        ProjectFactory(is_featured=True)
        ProjectFactory(is_featured=True)
        ProjectFactory(is_featured=False)
        response = api_client.get(f"{self.BASE_URL}?is_featured=true")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_project_technology_relationship(self, api_client):
        project = ProjectFactory()
        tech = TechnologiesFactory()
        project.technologies.add(tech)
        response = api_client.get(f"{self.BASE_URL}{project.id}/")
        assert response.status_code == status.HTTP_200_OK
        tech_ids = [t["id"] for t in response.data["technologies"]]
        assert tech.id in tech_ids

    def test_project_ordering_by_created_at_desc(self, api_client):
        p1 = ProjectFactory()
        p2 = ProjectFactory()
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == p2.id

    def test_project_str(self):
        project = ProjectFactory.build(title="My Project")
        assert str(project) == "My Project"
