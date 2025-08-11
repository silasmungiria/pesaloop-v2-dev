from django.core.cache import caches
from rbac.utils import CacheSettings

def clear_permission_cache(user):
    cache = caches['default']
    cache_key = f"{CacheSettings.CACHE_KEY_PREFIX}{user.id}"
    cache.delete(cache_key)
