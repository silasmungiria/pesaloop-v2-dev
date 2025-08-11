from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .role import Role
from userservice.models import User

class UserRole(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='user_assignments')
    notes = models.TextField(blank=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_role'
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')
        unique_together = ('user', 'role')
        ordering = ['user', '-assigned_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()
