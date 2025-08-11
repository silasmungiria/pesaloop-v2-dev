from django.core.cache import cache
from django.apps import apps
from mediaservice.services import ImageURLGenerator


class CustomerProfileFormatter:
    @staticmethod
    def _get_customer_model():
        return apps.get_model("userservice", "Customer")

    @staticmethod
    def prepare(customer_profile, use_cache=True):
        """
        Format a customer profile for API response.
        """
        CACHE_TIMEOUT = 3600  # 1 hour
        CACHE_KEY_PREFIX = "customer_profile_"
        cache_key = f"{CACHE_KEY_PREFIX}{customer_profile.id}"

        if use_cache:
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data

        selfie_image_url = (
            ImageURLGenerator.build(customer_profile, "selfie_image", "selfie")
            if customer_profile.selfie_image else None
        )

        profile_data = {
            "id": customer_profile.id,
            "id_type": customer_profile.id_type,  # Access via property
            "id_number": customer_profile.id_number,  # Access via property
            "selfie_image_url": selfie_image_url,
            "is_id_front_uploaded": bool(customer_profile.id_image_front),
            "is_id_back_uploaded": bool(customer_profile.id_image_back),
            "is_face_uploaded": bool(customer_profile.selfie_image),
            "is_address_proof_image_uploaded": bool(customer_profile.address_proof_image),
            "is_selfie_image_verified": customer_profile.is_selfie_image_verified,
            "is_id_front_verified": customer_profile.is_id_image_front_verified,
            "is_id_back_verified": customer_profile.is_id_image_back_verified,
            "is_address_proof_image_verified": customer_profile.is_address_proof_image_verified,
            "verification_status": customer_profile.verification_status,  # Access via property
            "customer_verified": customer_profile.customer_verified,  # Access via property
            "verification_date": customer_profile.verification_date,
            "remarks": customer_profile.remarks,  # Access via property
            "created_at": customer_profile.created_at,
            "updated_at": customer_profile.updated_at,
        }

        if use_cache:
            cache.set(cache_key, profile_data, timeout=CACHE_TIMEOUT)

        return profile_data

    @classmethod
    def get_optimized_queryset(cls):
        """
        Return a queryset optimized for profile formatting.
        Note: We can't use only() with encrypted fields as they're properties, not database fields.
        """
        Customer = cls._get_customer_model()
        return Customer.objects.select_related('user').defer(
            '_id_type',
            '_id_number',
            '_country',
            '_region_state',
            '_city',
            '_postal_code',
            '_postal_address',
            '_residential_address',
            '_next_of_kin_name',
            '_next_of_kin_relationship',
            '_next_of_kin_contact',
            '_verification_status',
            '_customer_verified',
            '_remarks'
        )
