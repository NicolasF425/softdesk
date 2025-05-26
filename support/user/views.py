from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserSerializer
from user.models import User


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Permissions différentes selon l'action
        """
        if self.action == 'create':
            # Seuls les admins peuvent créer des utilisateurs
            permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            # Tous les utilisateurs connectés peuvent voir les utilisateurs
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Seuls les admins ou le propriétaire peuvent modifier
            permission_classes = [IsAuthenticated]  # + logique personnalisée
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Endpoint public pour l'inscription"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'Utilisateur créé avec succès', 'user_id': user.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
