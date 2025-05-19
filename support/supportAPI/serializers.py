from rest_framework import serializers
from supportAPI.models import User, Contributor, Project, Issue, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['created_time']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


class ProjectDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'author', 'name', 'description', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']

    def create(self, validated_data):

        # TEMP
        user = User.objects.first()  # ou un utilisateur spécifique
        # Récupérer l'utilisateur de la requête
        # user = self.context['request'].user

        # Créer le projet avec les données fournies
        project = Project.objects.create(author=user, **validated_data)

        Contributor.objects.create(
            user=user,
            project=project,
        )

        return project


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'author', 'name', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']


class IssueDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'author', 'project', 'created_time']
        read_only_fields = ['created_time']


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'name', 'author', 'project', 'created_time']
        read_only_fields = ['created_time']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['created_time']
