from rest_framework import permissions
from django.core.cache import caches
from django.utils import timezone
import logging

from rbac.utils import CacheSettings

logger = logging.getLogger('security')

class BaseAccessPermission(permissions.BasePermission):
    PERMISSION_CACHE_TIMEOUT = CacheSettings.PERMISSION_CACHE_TIMEOUT
    CACHE_KEY_PREFIX = CacheSettings.CACHE_KEY_PREFIX

    def get_required_permission(self, request, view):
        print(f"Determining required permission for view: {view.__class__.__name__}")
        method = request.method.upper()
        if hasattr(view, f"{method}_permission"):
            print(f"Using {method}_permission attribute for view: {view.__class__.__name__}")
            return getattr(view, f"{method}_permission", None)
        if hasattr(view, 'required_permission'):
            print(f"Using required_permission attribute for view: {view.__class__.__name__}")
            return getattr(view, 'required_permission', None)
        return getattr(view, f"{method}_permission", None) or getattr(view, 'required_permission', None)

    def get_user_permissions(self, user):
        cache = caches['default']
        cache_key = f"{self.CACHE_KEY_PREFIX}{user.id}"

        if cached_perms := cache.get(cache_key):
            return cached_perms

        perms = set(
            user.roles.filter(is_active=True)
            .prefetch_related('role__permissions__permission')
            .values_list('role__permissions__permission__codename', 
                       'role__permissions__permission__method')
        )
        
        formatted_perms = {f"{codename}.{method}" for codename, method in perms if codename}
        cache.set(cache_key, formatted_perms, self.PERMISSION_CACHE_TIMEOUT)
        return formatted_perms
    
    def clear_permission_cache(self, user):
        cache = caches['default']
        cache_key = f"{self.CACHE_KEY_PREFIX}{user.id}"
        cache.delete(cache_key)

    def log_access_attempt(self, request, permission, granted):
        logger.info(
            f"Access {'granted' if granted else 'denied'} - "
            f"User: {request.user.id}, "
            f"Permission: {permission}, "
            f"Path: {request.path}, "
            f"Method: {request.method}, "
            f"Timestamp: {timezone.now()}"
        )
