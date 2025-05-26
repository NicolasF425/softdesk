from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    age = models.IntegerField(null=False, default=18)
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
