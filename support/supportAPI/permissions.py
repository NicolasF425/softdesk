from rest_framework import permissions
from .models import Contributor


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement au propriétaire
    de modifier/supprimer ses objets
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissions d'écriture seulement pour le propriétaire
        return obj.user == request.user  # ou obj.created_by selon votre modèle


class IsProjectContributor(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est contributeur du projet
    - Pour les issues : vérifie via issue.project
    - Pour les comments : vérifie via comment.issue.project
    """

    def has_permission(self, request, view):
        # Authentification requise
        if not (request.user and request.user.is_authenticated):
            return False

        # Pour les actions de création, vérifier les données POST
        if request.method == 'POST':
            if hasattr(view, 'get_project_from_request'):
                project = view.get_project_from_request(request)
                if project:
                    return Contributor.objects.filter(
                        user=request.user,
                        project=project
                    ).exists()

        return True

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous les contributeurs du projet
        if request.method in permissions.SAFE_METHODS:
            project = self._get_project_from_object(obj)
            return Contributor.objects.filter(
                user=request.user,
                project=project
            ).exists()

        # Écriture/modification autorisée seulement pour les contributeurs
        project = self._get_project_from_object(obj)
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
