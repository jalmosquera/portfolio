import pytest
from django.db import IntegrityError
from rest_framework import status
from .conftest import ProjectFactory, ProblemSolutionFactory


@pytest.mark.django_db
class TestProblemSolutionViewSet:
    BASE_URL = "/api/problem-solutions/"

    def test_list_problem_solutions(self, api_client):
        ProblemSolutionFactory.create_batch(2)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_problem_solution(self, api_client):
        project = ProjectFactory()
        data = {
            "project": project.id,
            "problem": "Restaurants lacked digital menus.",
            "solution": "Built a SaaS platform with QR codes.",
        }
        response = api_client.post(self.BASE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["problem"] == "Restaurants lacked digital menus."

    def test_retrieve_problem_solution(self, api_client):
        ps = ProblemSolutionFactory()
        response = api_client.get(f"{self.BASE_URL}{ps.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["problem"] == ps.problem

    def test_update_problem(self, api_client):
        ps = ProblemSolutionFactory()
        response = api_client.patch(f"{self.BASE_URL}{ps.id}/", {"problem": "Updated problem."})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["problem"] == "Updated problem."

    def test_delete_problem_solution(self, api_client):
        ps = ProblemSolutionFactory()
        response = api_client.delete(f"{self.BASE_URL}{ps.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_one_to_one_constraint(self):
        project = ProjectFactory()
        ProblemSolutionFactory(project=project)
        with pytest.raises(IntegrityError):
            ProblemSolutionFactory(project=project)

    def test_related_name_accessor(self):
        ps = ProblemSolutionFactory()
        assert ps.project.problem_solution == ps

    def test_problem_solution_str(self):
        ps = ProblemSolutionFactory.build()
        ps.project = ProjectFactory.build(title="Alternativa 2.0")
        assert str(ps) == "Alternativa 2.0"
