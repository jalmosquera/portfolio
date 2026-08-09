import pytest
from rest_framework import status
from .conftest import ProjectFactory, LessonFactory


@pytest.mark.django_db
class TestLessonViewSet:
    BASE_URL = "/api/lessons/"

    def test_list_lessons(self, api_client):
        LessonFactory.create_batch(3)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_filter_lessons_by_project(self, api_client):
        project = ProjectFactory()
        expected = LessonFactory(project=project)
        LessonFactory()

        response = api_client.get(self.BASE_URL, {"project": project.id})

        assert response.status_code == status.HTTP_200_OK
        assert [lesson["id"] for lesson in response.data] == [expected.id]

    def test_create_lesson(self, api_client):
        project = ProjectFactory()
        data = {"project": project.id, "text": "Multi-tenant architecture is complex."}
        response = api_client.post(self.BASE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "Multi-tenant architecture is complex."

    def test_retrieve_lesson(self, api_client):
        lesson = LessonFactory()
        response = api_client.get(f"{self.BASE_URL}{lesson.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == lesson.text

    def test_update_text(self, api_client):
        lesson = LessonFactory()
        response = api_client.patch(f"{self.BASE_URL}{lesson.id}/", {"text": "Updated lesson."})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == "Updated lesson."

    def test_delete_lesson(self, api_client):
        lesson = LessonFactory()
        response = api_client.delete(f"{self.BASE_URL}{lesson.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_lessons_related_name(self):
        project = ProjectFactory()
        LessonFactory.create_batch(4, project=project)
        assert project.lessons.count() == 4

    def test_lesson_str_truncation(self):
        long_text = "A" * 100
        lesson = LessonFactory.build(text=long_text)
        assert str(lesson) == "A" * 50
