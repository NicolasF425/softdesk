from django.contrib import admin
from supportAPI.models import Contributor, Project, Issue, Comment


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'project')


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description', 'author', 'created_time')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('id', 'project', 'author', 'description')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('id', 'author', 'issue', 'description',)


admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
