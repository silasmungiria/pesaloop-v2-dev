import random

from django.utils.timezone import now, timedelta
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from userservice import models as user_models
from authservice import models
from authservice.utils import OTP_EXPIRATION_MINUTES


token_generator = PasswordResetTokenGenerator()


class OTPManager:
    @staticmethod
    def generate_otp(user_id):
        user = user_models.User.objects.get(id=user_id)
        otp = f"{random.randint(100000, 999999)}"
        expires_at = now() + timedelta(minutes=OTP_EXPIRATION_MINUTES)
        models.OTP.objects.create(user=user, otp=otp, expires_at=expires_at)
        return otp

    @staticmethod
    def validate_otp(user_id, otp):
        otp_qs = models.OTP.objects.filter(
            user=user_id,
            is_used=False,
            expires_at__gt=now(),
        )

        for otp_instance in otp_qs:
            if otp_instance.otp == otp:
                otp_instance.is_used = True
                otp_instance.save()
                return True

        return False

