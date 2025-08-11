from django.conf import settings


class ImageURLGenerator:
    @staticmethod
    def build(instance, image_field_name: str, image_type: str) -> str | None:
        """Generate a full image URL for the specified image type."""
        image_field = getattr(instance, image_field_name, None)

        if image_field:
            return f"{settings.BACKEND_LOCAL_URL}/api/media/customer/images/{instance.id}/{image_type}/"
        return None
