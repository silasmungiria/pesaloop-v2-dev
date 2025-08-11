from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel


class Role(BaseModel):
    class Level(models.IntegerChoices):
        BASIC = 1, _('Basic')
        INTERMEDIATE = 2, _('Intermediate')
        SENIOR = 3, _('Senior')
        ADMINISTRATOR = 4, _('Administrator')
        SYSTEM = 5, _('System')

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    level = models.IntegerField(choices=Level.choices, default=Level.BASIC)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'role'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['level', 'name']
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['is_default']),
        ]

    def __str__(self):
        return f"{self.name} (Level {self.level})"
