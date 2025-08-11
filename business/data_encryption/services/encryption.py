from cryptography.fernet import Fernet, InvalidToken
from functools import lru_cache
from typing import Optional, Union
from django.conf import settings


class EncryptionService:
    """Service for encrypting and decrypting data using Fernet symmetric encryption."""

    @classmethod
    @lru_cache(maxsize=1)
    def _get_cipher_suite(cls) -> Fernet:
        """
        Returns the active Fernet encryption instance.
        Cached for performance since the key doesn't change during runtime.
        
        Raises:
            ValueError: If the key is missing or invalid
        """
        key = getattr(settings, "DB_ENCRYPTION_KEY", None)
        if not key:
            raise ValueError("Encryption key not found in settings")
        
        try:
            if isinstance(key, str):
                key = key.encode()
            return Fernet(key)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid encryption key: {e}") from e

    @classmethod
    def encrypt(cls, value: Optional[str]) -> Optional[bytes]:
        """
        Encrypts a string value using the active encryption key.
        
        Args:
            value: The string to encrypt (None returns None)
            
        Returns:
            Encrypted bytes or None if input was None
            
        Raises:
            ValueError: If value is empty or encryption fails
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            raise TypeError("Value to encrypt must be a string")
        if not value:
            raise ValueError("Value to encrypt cannot be empty")

        try:
            cipher_suite = cls._get_cipher_suite()
            return cipher_suite.encrypt(value.encode())
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}") from e

    @classmethod
    def decrypt(cls, value: Optional[Union[bytes, memoryview, bytearray]]) -> Optional[str]:
        """
        Decrypts an encrypted value using the active encryption key.
        
        Args:
            value: The encrypted data to decrypt (None returns None)
            
        Returns:
            Decrypted string or None if input was None
            
        Raises:
            ValueError: If decryption fails (invalid token or corrupted data)
        """
        if value is None:
            return None

        try:
            cipher_suite = cls._get_cipher_suite()
            
            # Convert memoryview or bytearray to bytes if needed
            if isinstance(value, (memoryview, bytearray)):
                value = bytes(value)
            elif not isinstance(value, bytes):
                raise TypeError("Value to decrypt must be bytes, memoryview, or bytearray")

            return cipher_suite.decrypt(value).decode()
        except InvalidToken as e:
            raise ValueError("Decryption failed - invalid token or corrupted data") from e
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}") from e
