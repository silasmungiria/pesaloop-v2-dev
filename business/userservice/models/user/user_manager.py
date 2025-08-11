from django.contrib.auth.models import BaseUserManager


class userManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, phone_number, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_number, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone_number, password, **extra_fields)

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('role', 'superuser')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('verified_email', True)
        extra_fields.setdefault('verified_phone_number', True)
        extra_fields.setdefault('is_loan_qualified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        return self._create_user(email, phone_number, password, **extra_fields)
