from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsProjectContributor
from supportAPI.models import Contributor, Issue, Comment
from supportAPI.serializers import ContributorSerializer
from supportAPI.serializers import ProjectDetailSerializer, ProjectListSerializer
from supportAPI.serializers import IssueDetailSerializer, IssueListSerializer, CommentSerializer


class ContributorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributor, IsOwnerOrReadOnly]
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        """
        Retourne seulement les issues des projets où l'utilisateur est contributeur
        """
        user_projects = Contributor.objects.filter(
            user=self.request.user
        ).values_list('project_id', flat=True)

        return Issue.objects.filter(project_id__in=user_projects).select_related('project', 'author')

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


class IssueViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributor, IsOwnerOrReadOnly]
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        """
        Retourne seulement les issues des projets où l'utilisateur est contributeur
        """
        user_projects = Contributor.objects.filter(
            user=self.request.user
        ).values_list('project_id', flat=True)

        queryset = Issue.objects.filter(project_id__in=user_projects).select_related('project', 'author')

        # Filtrage par projet si spécifié dans les paramètres GET
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributor, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
