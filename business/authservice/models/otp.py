import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from data_encryption.services import EncryptionService

User = get_user_model()


class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    encrypted_otp = models.BinaryField(null=True, blank=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'otp'
        verbose_name = 'One-Time Password'
        verbose_name_plural = 'One-Time Passwords'
        indexes = [
            models.Index(fields=['user', 'expires_at', 'is_used']),
        ]
        ordering = ['-expires_at']

    @property
    def otp(self):
        return EncryptionService.decrypt(self.encrypted_otp)

    @otp.setter
    def otp(self, value):
        self.encrypted_otp = EncryptionService.encrypt(value)

    def has_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP({self.otp}) for {self.user} expires at {self.expires_at}"
