import pprint
from django.core.management.base import BaseCommand
from data_encryption.services import KeyRotationService, KeyRotationError


class Command(BaseCommand):
    help = "Rotate the encryption key and re-encrypt all sensitive data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate key rotation without making any changes",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        self.stdout.write(self.style.MIGRATE_HEADING("Starting encryption key rotation..."))
        
        try:
            service = KeyRotationService()

            if dry_run:
                self.stdout.write(self.style.WARNING("Running in dry-run mode. No changes will be made."))
                self.stdout.write(self.style.MIGRATE_HEADING("Model Field Configuration:"))
                for model, fields in service.model_configurations:
                    self.stdout.write(f"- {model.__name__}: {fields}")
                self.stdout.write(self.style.SUCCESS("Dry-run completed successfully."))
            else:
                result = service.rotate_encryption_key_monthly()
                self.stdout.write(self.style.SUCCESS("Key rotation completed. Summary:"))
                self.stdout.write(pprint.pformat(result))

        except KeyRotationError as e:
            self.stderr.write(self.style.ERROR(f"Key rotation failed: {str(e)}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {str(e)}"))
