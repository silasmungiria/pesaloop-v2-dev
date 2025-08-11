# Data Encryption Module

## Overview

This module provides secure data encryption at rest for Django models, with key rotation capabilities. It includes:

1. **Encryption Service**: For encrypting/decrypting sensitive fields
2. **Key Rotation Service**: For periodic encryption key rotation
3. **Management Commands**: For manual key rotation
4. **Admin Notifications**: For rotation status alerts
5. **Celery Tasks**: For automated rotation scheduling

## Installation

1. Add to your Django project:

   ```python
   INSTALLED_APPS = [
       ...
       'data_encryption',
   ]
   ```

2. Configure required settings:

   ```python
   # Required
   DB_ENCRYPTION_KEY = env('DB_ENCRYPTION_KEY')  # Fernet-compatible key
   PAYLOAD_ENCRYPTION_KEY = env('PAYLOAD_ENCRYPTION_KEY')

   # Recommended
   ENCRYPTION_KEY_ROTATION = {
       'BACKUP_DIR': BASE_DIR / 'common' / 'backups' / 'keys',
       'BACKUP_FILENAME_FORMAT': 'encryption_key_{timestamp}.json',
       'KEY_ROTATION_SCHEDULE': 'monthly'  # or 'weekly'/'daily'
   }

   # For notifications
   EMAIL_FROM_ALERTS = 'alerts@yourdomain.com'
   EMAIL_SECURITY = 'security@yourdomain.com'
   ```

## Basic Usage

### Encrypting Model Fields

1. Import the encryption service:

   ```python
   from data_encryption.services import EncryptionService
   ```

2. Use in your models:

   ```python
   class Customer(models.Model):
       _ssn = models.BinaryField(null=True)

       @property
       def ssn(self):
           return EncryptionService.decrypt(self._ssn)

       @ssn.setter
       def ssn(self, value):
           self._ssn = EncryptionService.encrypt(value)
   ```

### Manual Key Rotation

```bash
python manage.py rotate_encryption_key
```

Options:

- `--dry-run`: Simulate without making changes
- `--force`: Skip confirmation prompts

## Integration Guide

### 1. Scheduled Rotation (Production)

Configure Celery beat schedule:

```python
CELERY_BEAT_SCHEDULE = {
    'rotate-encryption-keys': {
        'task': 'data_encryption.tasks.rotate_encryption_key_task',
        'schedule': crontab(day_of_month=1, hour=3),  # Monthly at 3AM
    },
}
```

### 2. Model Configuration

To customize which models/fields get encrypted:

1. Create `custom_rotation.py` in your app:

   ```python
   from data_encryption.services import KeyRotationService

   class CustomKeyRotationService(KeyRotationService):
       def _load_model_configurations(self):
           return [
               (YourModel, ['_field1', '_field2']),
               ...
           ]
   ```

2. Update settings:
   ```python
   DATA_ENCRYPTION_SERVICE = 'yourapp.custom_rotation.CustomKeyRotationService'
   ```

### 3. Notification Customization

Override the default notifier:

```python
class CustomNotifier(EncryptionKeyRotationNotifier):
    def send_key_rotation_notification(self, details):
        # Custom logic (Slack, SMS, etc.)
        ...
```

## Backup and Recovery

### Key Backup Location

Rotated keys are stored in:

```
<BACKUP_DIR>/encryption_key_<TIMESTAMP>.json
```

Example recovery process:

1. Locate the backup JSON file
2. Update settings:
   ```python
   DB_ENCRYPTION_KEY = 'key_from_backup_file'
   ```
3. Restart application

## Security Considerations

1. **Key Storage**:

   - Never commit keys to version control
   - Restrict backup directory permissions
   - Consider AWS KMS/HSM for production

2. **Rotation Policy**:

   - Monthly rotation recommended
   - Immediate rotation if key compromise suspected

3. **Database Backups**:
   - Always backup before rotation
   - Test recovery procedure regularly

## Troubleshooting

### Common Issues

**Q: Getting "InvalidToken" errors after rotation?**
A: This indicates some data wasn't properly re-encrypted. Restore from backup and:

1. Verify all models are in `model_configurations`
2. Check for direct database manipulations bypassing Django ORM

**Q: Notification emails not sending?**
A: Verify:

1. Email settings are properly configured
2. SMTP server is accessible
3. Admin emails are valid

## API Reference

### KeyRotationService

```python
rotate_encryption_key_monthly() -> dict
"""
Performs full rotation cycle. Returns:
{
    'status': 'completed'|'failed',
    'timestamp': 'ISO8601',
    'models_processed': int,
    'records_processed': int,
    'failed_records': int,
    'key_backup_path': str
}
"""
```

### EncryptionService

```python
encrypt(value: str) -> bytes
decrypt(value: bytes) -> str
```

## Development

### Testing

Run the test suite with:

```bash
python manage.py test data_encryption --settings=your.test_settings
```

### Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request with tests

---
