# Standard Imports
import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Type

# Third-Party Imports
from cryptography.fernet import Fernet, InvalidToken
from django.db import models, transaction
from django.conf import settings

# Project Specific Imports
from . import EncryptionService


class KeyRotationService:
    """Service for handling encryption key rotation and data re-encryption."""
    
    def __init__(self):
        self.model_configurations = self._load_model_configurations()

    @staticmethod
    def generate_key() -> str:
        """Generates a new Fernet encryption key."""
        return Fernet.generate_key().decode()

    @staticmethod
    def _get_dump_directory() -> Path:
        """Get backup directory from settings"""
        return settings.ENCRYPTION_KEY_ROTATION['BACKUP_DIR']

    @staticmethod
    def _save_key_to_file(key: str, timestamp: str) -> str:
        """Saves the encryption key to a JSON file with timestamp."""
        key_file = settings.ENCRYPTION_KEY_ROTATION['BACKUP_FILENAME_FORMAT'].format(timestamp=timestamp)
        key_file_path = Path(KeyRotationService._get_dump_directory()) / key_file
        
        key_data = {
            "key": key,
            "generated_at": timestamp,
            "rotation_status": "completed"
        }

        with open(key_file_path, "w") as file:
            json.dump(key_data, file, indent=4)

        return str(key_file_path)

    def _load_model_configurations(self) -> List[Tuple[Type[models.Model], List[str]]]:
        """Returns list of (model, fields) tuples that need encryption."""
        try:
            from authservice import models as credential_models
            from walletservice import models as wallets_models
            from userservice import models as user_models
            from paymentservice import models as payment_models

            return [
                (credential_models.OTP, ["_otp"]),
                (wallets_models.DigitalWallet, ["_balance"]),
                (user_models.Customer, [
                    "_id_type", "_id_number", "_country", "_region_state",
                    "_city", "_postal_code", "_postal_address", "_residential_address",
                    "_verification_status", "_remarks", "_customer_verified"
                ]),
                (payment_models.TransactionRecord, ["_amount"]),
                (payment_models.RequestedTransaction, ["_amount"])
            ]
        except ImportError as e:
            raise ImportError(f"Failed to import required models: {e}")

    @staticmethod
    def _re_encrypt_record(record: models.Model, fields: List[str]) -> bool:
        """Re-encrypts fields for a single record."""
        try:
            for field in fields:
                if (current_value := getattr(record, field)) is None:
                    continue
                    
                if (decrypted := EncryptionService.decrypt(current_value)) is not None:
                    setattr(record, field, EncryptionService.encrypt(decrypted))
            
            record.save()
            return True
        except (InvalidToken, ValueError, AttributeError) as e:
            print(f"Error re-encrypting {record.__class__.__name__} ID {record.pk}: {str(e)}")
            return False

    def rotate_encryption_key_monthly(self) -> dict:
        """Performs full key rotation and returns status report."""
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        report = {
            "status": "started", "timestamp": timestamp,
            "models_processed": 0, "records_processed": 0,
            "failed_records": 0, "key_backup_path": None
        }

        try:
            with transaction.atomic():
                new_key = self.generate_key()
                
                for model, fields in self.model_configurations:
                    report["models_processed"] += 1
                    for record in model.objects.iterator():
                        if self._re_encrypt_record(record, fields):
                            report["records_processed"] += 1
                        else:
                            report["failed_records"] += 1

                settings.DB_ENCRYPTION_KEY = new_key
                report["key_backup_path"] = self._save_key_to_file(new_key, timestamp)
                
                from ..tasks import notify_admin_encryption_key_rotation_task
                notify_admin_encryption_key_rotation_task.delay(**{
                    k: report[k] for k in ['timestamp', 'models_processed', 
                                          'records_processed', 'failed_records']
                })

                report["status"] = "completed"
                return report

        except Exception as e:
            report.update({"status": "failed", "error": str(e)})
            raise KeyRotationError("Key rotation failed") from e


class KeyRotationError(Exception):
    """Custom exception for key rotation failures."""
    pass
