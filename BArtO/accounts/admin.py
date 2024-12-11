from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser
from django.contrib.auth.models import Group


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ['username', 'email', 'role', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_active']
    ordering = ['date_joined']
    readonly_fields = ['date_joined']
    filter_horizontal = ['groups', 'user_permissions']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.is_superuser:
            obj.role = 'admin'

        else:
            editors_group = Group.objects.get(name='Editors')
            if editors_group in obj.groups.all():
                obj.role = 'editor'
            else:
                obj.role = 'artist'

        obj.save()
