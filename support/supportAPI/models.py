from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Project():
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor():
    user = User
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class ProjectContributors():
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(to=Contributor)


class Issue():
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(to=Contributor)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment():
    Issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    contributor = models.ForeignKey(to=Contributor)
    created_time = models.DateTimeField(auto_now_add=True)
