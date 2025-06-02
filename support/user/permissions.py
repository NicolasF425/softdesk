from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement aux propriétaires
    d'un objet ou aux admins de le modifier/supprimer.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Permissions d'écriture seulement pour le propriétaire ou l'admin
        return obj == request.user or request.user.is_superuser
