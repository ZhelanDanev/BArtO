from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser

# Регистрираме AppUser в Django Admin
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_active']
    ordering = ['date_joined']

# Регистрирме AppUserAdmin
admin.site.register(AppUser, AppUserAdmin)
