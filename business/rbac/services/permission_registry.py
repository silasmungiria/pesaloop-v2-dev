from django.apps import apps
from django.urls import get_resolver
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from rbac.models import Permission

def register_model_permissions(model):
    basename = getattr(model, 'permission_basename', None)
    if not basename:
        return

    permissions = [
        ('view', 'GET'),
        ('add', 'POST'),
        ('change', 'PUT'),
        ('change', 'PATCH'),
        ('delete', 'DELETE'),
        ('all', 'ALL')
    ]

    for perm_name, method in permissions:
        codename = f"{basename}_{perm_name}"
        Permission.objects.get_or_create(
            codename=codename,
            method=method,
            defaults={
                'name': f"{perm_name.capitalize()} {model._meta.verbose_name}",
                'category': Permission.Category.SYSTEM,
                'description': (
                    f"Grants the ability to perform the HTTP {method.upper()} operation "
                    f"({perm_name}) on the {model._meta.verbose_name} model. "
                    f"This includes access to API endpoints or logic that supports this action."
                ),
            }
        )

def register_view_permissions(view_class):
    """Automatically register permissions for a view class across all apps"""
    
    model_name = None
    model_verbose_name = None
    
    # Method 1: Check for queryset attribute (DRF ModelViewSet)
    if hasattr(view_class, 'queryset') and view_class.queryset is not None:
        model = view_class.queryset.model
        model_name = model._meta.model_name
        model_verbose_name = model._meta.verbose_name.lower()
    
    # Method 2: Check for get_queryset method
    elif hasattr(view_class, 'get_queryset'):
        try:
            model = view_class().get_queryset().model
            model_name = model._meta.model_name
            model_verbose_name = model._meta.verbose_name.lower()
        except:
            pass
    
    # Method 3: Check for serializer_class (DRF views)
    elif hasattr(view_class, 'serializer_class'):
        try:
            model = view_class.serializer_class.Meta.model
            model_name = model._meta.model_name
            model_verbose_name = model._meta.verbose_name.lower()
        except:
            pass
    
    # Method 4: Parse from view class name
    if model_name is None:
        class_name = view_class.__name__.lower()
        if class_name.endswith('viewset'):
            potential_model = class_name[:-7]  # Remove 'viewset'
            # Verify if this matches an actual model
            for model in apps.get_models():
                if model._meta.model_name == potential_model:
                    model_name = potential_model
                    model_verbose_name = model._meta.verbose_name.lower()
                    break
    
    # Register default CRUD permissions if we found a model
    if model_name:
        default_permissions = {
            'get': 'view',
            'post': 'add',
            'put': 'change',
            'patch': 'change',
            'delete': 'delete',
        }
        
        for method, perm_type in default_permissions.items():
            permission_codename = f"{perm_type}_{model_name}"
            
            # Check for explicit permission definition first
            explicit_perm = getattr(view_class, f"{method}_permission", None)
            if explicit_perm:
                permission_codename = explicit_perm
            
            Permission.objects.get_or_create(
                codename=permission_codename,
                method=method.upper(),
                defaults={
                    'name': f"{perm_type.capitalize()} {model_verbose_name or model_name}",
                    'category': Permission.Category.SYSTEM,
                    'description': (
                        f"Grants access to perform the {perm_type.upper()} operation via HTTP "
                        f"{method.upper()} method on endpoints related to {model_verbose_name or model_name}. "
                        "Typically used in ViewSets or API views to restrict access by action."
                    ),
                }
            )
    
    # Register any explicitly defined permissions that weren't covered by CRUD
    for method in ['get', 'post', 'put', 'patch', 'delete']:
        if perm_codename := getattr(view_class, f"{method}_permission", None):
            Permission.objects.get_or_create(
                codename=perm_codename,
                method=method.upper(),
                defaults={
                    'name': f"{method.upper()} access: {perm_codename.replace('_', ' ').capitalize()}",
                    'category': Permission.Category.SYSTEM,
                    'description': (
                        f"Grants explicit permission to perform the {method.upper()} operation defined "
                        f"by `{perm_codename}`. Intended for custom actions or overrides outside standard CRUD."
                    ),
                }
            )

def scan_url_permissions(resolver):
    """Scan URL patterns and register permissions for all views"""
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):
            scan_url_permissions(pattern)
        elif hasattr(pattern, 'callback'):
            process_view_permissions(pattern.callback)

def process_view_permissions(view):
    """Process a single view to register permissions"""
    if hasattr(view, 'view_class'):
        register_view_permissions(view.view_class)
    elif hasattr(view, 'cls'):
        register_view_permissions(view.cls)
    elif hasattr(view, '__name__') and view.__name__ == 'view':
        try:
            register_view_permissions(view.view_class)
        except:
            pass

@receiver(post_migrate)
def register_permissions(sender, **kwargs):
    """Main registration function that ties everything together"""
    # Register model permissions
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if hasattr(model, 'permission_basename'):
                register_model_permissions(model)

    # Register view permissions from URLs
    scan_url_permissions(get_resolver())
