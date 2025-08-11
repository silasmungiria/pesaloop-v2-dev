import jwt
from datetime import datetime, timedelta
from django.conf import settings


class JWTUtils:
    @staticmethod
    def encode_ref(reference_id: str) -> str:
        """
        Create a short-lived JWT for callback validation.
        """
        payload = {
            "ref": reference_id,
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decode and validate a callback JWT.
        """
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
