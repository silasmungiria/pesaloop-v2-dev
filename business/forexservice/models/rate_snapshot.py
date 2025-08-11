from django.db import models
from .base import BaseModel


class RateSnapshot(BaseModel):
    response_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'rate_snapshots'
        verbose_name = 'Rate Snapshot'
        verbose_name_plural = 'Rate Snapshots'
        ordering = ['-created_at']

    def __str__(self):
        return f"Exchange rates for {self.created_at}"
