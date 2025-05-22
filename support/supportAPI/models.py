from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    age = models.IntegerField(null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    # Fix the groups field with a unique related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='supportapi_user_set',  # This is the fix
        related_query_name='user',
    )

    # Fix the user_permissions field with a unique related_name
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='supportapi_user_set',  # This is the fix
        related_query_name='user',
    )


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default="Projet")
    description = models.CharField(max_length=1024, default="Description")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    TYPE_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task')
    ]

    STATUS_CHOICES = [
        ('TO DO', 'To Do'),
        ('IN PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128,  default="Issue")
    description = models.CharField(max_length=1024,  default="Description")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='TASK'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='TO DO'
    )


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1024, default="Commentaire")
