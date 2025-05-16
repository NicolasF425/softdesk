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


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author']
        read_only_fields = ['created_time']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'author', 'project']
        read_only_fields = ['created_time']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue']
        read_only_fields = ['created_time']
