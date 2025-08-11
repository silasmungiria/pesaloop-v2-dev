# common/encryption.py
from data_encryption.services import EncryptionService

class EncryptedFieldsMixin:
    """
    Mixin to provide automatic encryption/decryption for fields.
    Models using this must define:
      encrypted_fields = ["field1", "field2", ...]
    The database fields should be named: encrypted_<field>
    """

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Dynamically create property accessors for encrypted fields.
        Runs when a subclass is created.
        """
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "encrypted_fields"):
            for field in cls.encrypted_fields:
                setattr(
                    cls,
                    field,
                    property(
                        lambda self, f=field: self._get_encrypted_field(f),
                        lambda self, value, f=field: self._set_encrypted_field(f, value)
                    )
                )

    def _get_encrypted_field(self, field_name):
        """
        Decrypts the encrypted_<field_name> value from the database.
        """
        raw_value = getattr(self, f"encrypted_{field_name}")
        return EncryptionService.decrypt(raw_value) if raw_value else None

    def _set_encrypted_field(self, field_name, value):
        """
        Encrypts the value and stores it in encrypted_<field_name>.
        """
        encrypted_value = EncryptionService.encrypt(value) if value is not None else None
        setattr(self, f"encrypted_{field_name}", encrypted_value)
