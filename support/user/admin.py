from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'birthdate', 'can_be_contacted', 'can_data_be_shared')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('birthdate', 'can_be_contacted', 'can_data_be_shared')}),
    )

    # Pour l'ajout d'utilisateurs
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('birthdate', 'can_be_contacted', 'can_data_be_shared')}),
    )


admin.site.register(User, UserAdmin)
