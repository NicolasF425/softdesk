from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import models

from user.permissions import IsOwnerOrSuperUser
from user.serializers import UserSerializer
from user.models import User


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Permissions différentes selon l'action
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve']:
            # Tous les utilisateurs connectés peuvent voir les utilisateurs
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Seuls les admins ou le propriétaire peuvent modifier
            permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
        elif self.action == 'logout':
            # Seuls les utilisateurs connectés peuvent se déconnecter
            permission_classes = [IsAuthenticated]
        elif self.action == 'me':
            # Action pour récupérer son propre profil
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filtre les utilisateurs selon l'action et les permissions
        """
        if self.action in ['list']:
            # Pour la liste, ne montrer que les utilisateurs qui acceptent le partage
            return User.objects.filter(can_data_be_shared=True)
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Pour les actions sur un utilisateur spécifique, permettre l'accès
            # si c'est le propriétaire ou un admin
            if self.request.user.is_superuser:
                return User.objects.all()
            else:
                # L'utilisateur peut accéder à son propre profil même si can_data_be_shared=False
                return User.objects.filter(
                    models.Q(can_data_be_shared=True) |
                    models.Q(id=self.request.user.id)
                )
        else:
            return User.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Utilisateur supprimé avec succès"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Déconnexion de l'utilisateur actuel avec blacklist du refresh token
        """
        try:
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response(
                    {'error': 'Le refresh token est requis pour la déconnexion'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Blacklister le refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    'message': f'Utilisateur {request.user.username} déconnecté avec succès',
                    'user': request.user.username
                },
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {'error': 'Token invalide ou déjà blacklisté'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {'error': 'Erreur lors de la déconnexion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Récupérer les informations de l'utilisateur connecté
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
