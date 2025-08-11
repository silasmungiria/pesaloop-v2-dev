from django.db.models.signals import post_migrate
from django.dispatch import receiver
from rbac.models import Role


@receiver(post_migrate)
def create_default_role(sender, **kwargs):
    if Role.objects.count() == 0:
        # Role.objects.create(
        #     name='Customer',
        #     description='Default customer role',
        #     level=Role.Level.BASIC,
        #     is_default=True
        # )
        basic_role = Role.objects.create(
            name="Basic User",
            level=Role.Level.BASIC,
            is_default=True,
            description="Default access level for all users"
        )

        intermediate_role = Role.objects.create(
            name="Intermediate User",
            level=Role.Level.INTERMEDIATE,
            is_default=False,
            description="Intermediate access level for users"
        )

        senior_role = Role.objects.create(
            name="Senior User",
            level=Role.Level.SENIOR,
            is_default=False,
            description="Senior access level for users"
        )

        admin_role = Role.objects.create(
            name="Administrator",
            level=Role.Level.ADMINISTRATOR,
            is_default=False,
            description="Administrator access with elevated permissions"
        )

        system_role = Role.objects.create(
            name="System",
            level=Role.Level.SYSTEM,
            is_default=False,
            description="System-level access with all permissions"
        )
