import pytest
from rest_framework import status
from .conftest import ProjectFactory, ProjectImageFactory


@pytest.mark.django_db
class TestProjectImageViewSet:
    BASE_URL = "/api/project-images/"

    def test_list_project_images(self, api_client):
        ProjectImageFactory.create_batch(3)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_filter_project_images_by_project(self, api_client):
        project = ProjectFactory()
        expected = ProjectImageFactory(project=project)
        ProjectImageFactory()

        response = api_client.get(self.BASE_URL, {"project": project.id})

        assert response.status_code == status.HTTP_200_OK
        assert [image["id"] for image in response.data] == [expected.id]

    def test_create_project_image(self, api_client):
        project = ProjectFactory()
        data = {"project": project.id, "title": "Admin Dashboard", "order": 0}
        response = api_client.post(self.BASE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Admin Dashboard"
        assert response.data["project"] == project.id

    def test_retrieve_project_image(self, api_client):
        img = ProjectImageFactory()
        response = api_client.get(f"{self.BASE_URL}{img.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == img.title

    def test_update_order(self, api_client):
        img = ProjectImageFactory(order=0)
        response = api_client.patch(f"{self.BASE_URL}{img.id}/", {"order": 5})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["order"] == 5

    def test_delete_project_image(self, api_client):
        img = ProjectImageFactory()
        response = api_client.delete(f"{self.BASE_URL}{img.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_gallery_related_name(self):
        project = ProjectFactory()
        ProjectImageFactory.create_batch(3, project=project)
        assert project.gallery.count() == 3
