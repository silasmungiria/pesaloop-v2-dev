from django.db import models
from .base import BaseModel


class Currency(BaseModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    class Meta:
        db_table = 'currency'
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        unique_together = ('code', 'name')
        indexes = [
            models.Index(fields=['code', 'name']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.code
