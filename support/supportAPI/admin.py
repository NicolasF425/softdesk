from django.contrib import admin
from supportAPI.models import User, Contributor, Project, Issue, Comment


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared')


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'project')


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description', 'author')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('name', 'description')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('description',)


admin.site.register(User, UserAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
