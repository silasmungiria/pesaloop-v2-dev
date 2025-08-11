from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .permission import Permission
from .role import Role
from userservice.models import User

class RolePermission(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, related_name='role_assignments')
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'role_permission'
        verbose_name = _('Role Permission')
        verbose_name_plural = _('Role Permissions')
        unique_together = ('role', 'permission')
        ordering = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission}"
