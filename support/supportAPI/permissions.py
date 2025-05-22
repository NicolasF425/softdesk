from rest_framework import permissions


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
