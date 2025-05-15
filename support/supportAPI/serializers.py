from rest_framework import serializers
from supportAPI.models import User, Contributor, Project, Issue, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'date_created', 'username']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'created_time', 'name', 'description']


class IssueSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'name', 'description', 'user', 'project']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_time', 'description', 'user', 'issue']
