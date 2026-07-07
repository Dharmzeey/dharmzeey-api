from rest_framework import generics, permissions

from .models import Project
from .serializers import ProjectSerializer, ProjectWriteSerializer


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    pagination_class = None

    def get_queryset(self):
        return Project.objects.filter(is_published=True)


class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Project.objects.filter(is_published=True)


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectWriteSerializer
    permission_classes = [permissions.IsAdminUser]


class ProjectUpdateView(generics.UpdateAPIView):
    serializer_class = ProjectWriteSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"
    queryset = Project.objects.all()


class ProjectDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"
    queryset = Project.objects.all()
