from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel


class Permission(BaseModel):
    class Category(models.TextChoices):
        USER = 'USER', _('User Management')
        TRANSACTION = 'TRANSACTION', _('Transactions')
        LOAN = 'LOAN', _('Loan Operations')
        REPORT = 'REPORT', _('Reporting')
        SYSTEM = 'SYSTEM', _('System Administration')

    class Method(models.TextChoices):
        GET = 'GET', 'GET'
        POST = 'POST', 'POST'
        PUT = 'PUT', 'PUT'
        PATCH = 'PATCH', 'PATCH'
        DELETE = 'DELETE', 'DELETE'
        ALL = 'ALL', 'ALL'

    name = models.CharField(max_length=128)
    codename = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.SYSTEM)
    method = models.CharField(max_length=6, choices=Method.choices, default=Method.ALL)
    is_sensitive = models.BooleanField(default=False)

    class Meta:
        db_table = 'permission'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        unique_together = ('codename', 'method')
        ordering = ['name', 'category', 'method']
        indexes = [
            models.Index(fields=['codename']),
            models.Index(fields=['category']),
            models.Index(fields=['method']),
        ]

    def __str__(self):
        method_str = f" ({self.method})" if self.method != 'ALL' else ''
        return f"{self.name}{method_str}, {self.codename} [{self.get_category_display()}]"
