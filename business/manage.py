#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def ensure_runtime_directories():
    """Create required runtime directories before initializing Django."""
    BASE_DIR = Path(__file__).resolve().parent
    (BASE_DIR / "common/artifacts").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "common/artifacts/logs").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "common/backups/keys").mkdir(parents=True, exist_ok=True)


def main():
    """Run administrative tasks."""
    ensure_runtime_directories()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pesaloop.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
