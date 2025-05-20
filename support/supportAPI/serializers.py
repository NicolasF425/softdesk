from rest_framework import serializers
from supportAPI.models import User, Contributor, Project, Issue, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'created_time']
        read_only_fields = ['created_time']


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
