from rest_framework import serializers
from models import User, Project, Issue, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'date_created', 'username']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'date_created', 'username', 'contributors', 'issues']


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'date_created', 'contributor', 'comments', 'project']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'date_created', 'contributor', 'issue']
