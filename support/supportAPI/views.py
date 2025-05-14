from rest_framework.viewsets import ReadOnlyModelViewSet

from models import Project, Issue, Comment
from serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(active=True)


class IssueViewset(ReadOnlyModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(active=True)


class CommentViewset(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(active=True)
