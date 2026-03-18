from apps.projects.models import Projects
from apps.projects.api.serializers import SerializerProjects
from rest_framework import vietset




class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = SerializerProjects






