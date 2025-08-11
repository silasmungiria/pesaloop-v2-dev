from django.contrib import admin
from .models import Permission, Role, RolePermission, UserRole

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'method', 'category', 'is_sensitive')
    list_filter = ('method', 'category', 'is_sensitive')
    search_fields = ('name', 'codename')
    ordering = ('category', 'name')

class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    raw_id_fields = ('permission',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'is_default')
    list_filter = ('level', 'is_default')
    search_fields = ('name',)
    inlines = [RolePermissionInline]

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_by', 'assigned_at', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('user__username', 'role__name')
    raw_id_fields = ('user', 'assigned_by')
    date_hierarchy = 'assigned_at'

admin.site.register(RolePermission)
