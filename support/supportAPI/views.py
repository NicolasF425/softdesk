from rest_framework.viewsets import ReadOnlyModelViewSet

from supportAPI.models import Project, Issue, Comment
from supportAPI.serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewset(ReadOnlyModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewset(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
