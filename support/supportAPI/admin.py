from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from supportAPI.models import User, Contributor, Project, Issue, Comment


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('age', 'can_be_contacted', 'can_data_be_shared')}),
    )

    # Pour l'ajout d'utilisateurs
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('age', 'can_be_contacted', 'can_data_be_shared')}),
    )


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'project')


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description', 'author', 'created_time')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('id', 'author', 'description')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('id', 'author', 'issue', 'description',)


admin.site.register(User, UserAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
