from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsProjectContributor
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from supportAPI.models import Contributor, Project, Issue, Comment
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
        Retourne seulement les projets où l'utilisateur est contributeur
        """
        user_projects = Contributor.objects.filter(
            user=self.request.user
        ).values_list('project_id', flat=True)

        return Project.objects.filter(id__in=user_projects)

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

    def get_project_from_request(self, request):
        """Méthode pour récupérer le projet depuis les données de la requête"""
        project_id = request.data.get('project')
        if project_id:
            try:
                return Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return None
        return None

    @action(detail=False, methods=['get'])
    def my_issues(self, request):
        """
        Action personnalisée pour récupérer seulement les issues créées par l'utilisateur
        """
        issues = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Créer une issue en assignant automatiquement l'auteur
        """
        # Vérifier que le projet existe et que l'utilisateur en est contributeur
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, id=project_id)

        # Double vérification de sécurité
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionError("Vous devez être contributeur du projet pour créer une issue.")

        serializer.save(author=self.request.user, project=project)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributor, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
