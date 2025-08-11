from django.apps import AppConfig

class RBACConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'

    def ready(self):
        # Import signal handlers only
        import rbac.signals.handlers
        import rbac.signals.auto_assign_default_role
        import rbac.signals.create_default_role
