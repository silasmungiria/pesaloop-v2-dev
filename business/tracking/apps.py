from django.apps import AppConfig

class TrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking'

    def ready(self):
        # Import moved to new location
        from django.db.models.functions import Now
        from django.core.serializers.python import Serializer as PythonSerializer
        from django.utils.encoding import is_protected_type

        def _patched_value_from_field(self, obj, field):
            value = field.value_from_object(obj)
            if isinstance(value, Now):
                return str(value)
            return value if is_protected_type(value) else field.value_to_string(obj)

        PythonSerializer._value_from_field = _patched_value_from_field
