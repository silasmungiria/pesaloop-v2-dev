import sys
from functools import wraps
from django.core.exceptions import PermissionDenied
from rbac.services import register_view_permissions



def permission_required(perm_codename, method='ALL'):
    """
    Decorator for view functions to check permissions
    Usage:
        @permission_required('manage_users', 'POST')
        def create_user(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.has_perm(perm_codename, method):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

def register_permissions(cls):
    """
    Class decorator to automatically register view permissions
    Usage:
        @register_permissions
        class MyViewSet(ViewSet):
            get_permission = 'view_thing'
            ...
    """
    if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
        return cls  # Skip registration during DB setup

    register_view_permissions(cls)
    return cls
