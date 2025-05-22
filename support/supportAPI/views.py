from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly
from supportAPI.models import User, Contributor, Project, Issue, Comment
from supportAPI.serializers import UserSerializer, ContributorSerializer
from supportAPI.serializers import ProjectDetailSerializer, ProjectListSerializer
from supportAPI.serializers import IssueDetailSerializer, IssueListSerializer, CommentSerializer


class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class ContributorViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class ProjectViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        # Sauvegarder le projet avec l'auteur
        project = serializer.save(author=self.request.user)

        # Créer le contributeur automatiquement
        Contributor.objects.create(
            user=self.request.user,
            project=project,
        )


class IssueViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
