from django.contrib import admin
# default django user admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# translates the text to human readable format
from django.utils.translation import gettext as _
# import our models from the core app
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    # If you want to add some extra fields such
    # as logout or last seen it can also be added quite easily
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# register the User and the UserAdmin class to that model
admin.site.register(models.User, UserAdmin)
