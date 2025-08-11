# from django.db.models.signals import post_migrate, post_save
# from django.dispatch import receiver
# from rbac.models import Permission
# from rbac.apps import RBACConfig

# @receiver(post_migrate)
# def handle_post_migrate(sender, **kwargs):
#     """Re-register permissions after migrations"""
#     if sender.name == 'rbac':
#         RBACConfig.register_existing_views(RBACConfig.create('rbac'))

# @receiver(post_save, sender=Permission)
# def update_permission_cache(sender, instance, **kwargs):
#     """
#     Clear relevant permission caches when permissions change
#     """
#     from rbac.services import clear_permission_cache
#     for user_role in instance.role_assignments.all():
#         clear_permission_cache(user_role.user)


from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from rbac.models import Permission
from rbac.services.permission_registry import register_view_permissions
from django.urls import get_resolver


@receiver(post_migrate)
def handle_post_migrate(sender, **kwargs):
    """Re-register permissions after migrations"""
    if sender.name == 'rbac':
        resolver = get_resolver()
        for url_pattern in resolver.url_patterns:
            if hasattr(url_pattern, 'callback') and hasattr(url_pattern.callback, 'view_class'):
                register_view_permissions(url_pattern.callback.view_class)


@receiver(post_save, sender=Permission)
def update_permission_cache(sender, instance, **kwargs):
    """Clear relevant permission caches when permissions change"""
    from rbac.services import clear_permission_cache
    for user_role in instance.role_assignments.all():
        clear_permission_cache(user_role.user)
