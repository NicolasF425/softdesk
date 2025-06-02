from rest_framework import permissions
from .models import Project, Contributor


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement au propriétaire (author)
    de modifier/supprimer ses objets
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissions d'écriture seulement pour le propriétaire
        return obj.author == request.user


class IsProjectContributor(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est contributeur du projet
    """

    def has_permission(self, request, view):
        # Authentification requise
        if not (request.user and request.user.is_authenticated):
            return False

        # Pour les actions de création, vérifier les données POST
        if request.method == 'POST':
            project_id = request.data.get('project')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id)
                    return Contributor.objects.filter(
                        user=request.user,
                        project=project
                    ).exists()
                except (Project.DoesNotExist, ValueError):
                    return False

        return True

    def has_object_permission(self, request, view, obj):
        project = self._get_project_from_object(obj)
        if not project:
            return False

        return Contributor.objects.filter(
            user=request.user,
            project=project
        ).exists()

    def _get_project_from_object(self, obj):
        """Récupère le projet selon le type d'objet"""
        if hasattr(obj, 'project'):  # Issue
            return obj.project
        elif hasattr(obj, 'issue'):  # Comment
            return obj.issue.project
        return None
