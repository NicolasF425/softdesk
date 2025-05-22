from rest_framework import serializers
from supportAPI.models import User, Contributor, Project, Issue, Comment
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'created_time', 'password', 'password2']
        read_only_fields = ['created_time']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        # Supprimer password2 car il n'est pas dans le modèle User
        validated_data.pop('password2')

        # Créer l'utilisateur
        user = User.objects.create(
            username=validated_data['username'],
            age=validated_data.get('age'),
            # Ajoutez d'autres champs si nécessaire
        )

        # Définir le mot de passe correctement (avec hachage)
        user.set_password(validated_data['password'])
        user.save()

        return user


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']
        read_only_fields = ['id']


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Project
        fields = ['id', 'author', 'name', 'description', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Project
        fields = ['id', 'author', 'name', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']


class IssueDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'author', 'project', 'priority', 'type', 'status',
                  'created_time']
        read_only_fields = ['id', 'author', 'project', 'created_time']


class IssueListSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )

    class Meta:
        model = Issue
        fields = ['id', 'name', 'author', 'project', 'priority', 'type', 'status', 'created_time']
        read_only_fields = ['id', 'author', 'project', 'created_time']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['id', 'created_time']
