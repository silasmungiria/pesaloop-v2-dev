from django.core.management.base import BaseCommand
from rbac.apps import RBACConfig

class Command(BaseCommand):
    help = 'Register all view permissions in the database'

    def handle(self, *args, **options):
        rbac_app = RBACConfig.create('rbac')
        rbac_app.register_existing_views()
        self.stdout.write(self.style.SUCCESS('Successfully registered all permissions'))
