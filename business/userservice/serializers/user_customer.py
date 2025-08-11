from rest_framework import serializers
from django.conf import settings
from django.core.validators import RegexValidator
from drf_spectacular.utils import extend_schema_field

from mediaservice.services import ImageURLGenerator
from userservice import models
from ..utils import CustomerDocType, CustomerStatus


class CustomerDocInfoSerializer(serializers.Serializer):
    id_type = serializers.ChoiceField(choices=CustomerDocType.CHOICES)
    id_number = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    country = serializers.CharField(max_length=100)
    region_state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=100)
    postal_address = serializers.CharField()
    residential_address = serializers.CharField()
    next_of_kin_name = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    next_of_kin_relationship = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    next_of_kin_contact = serializers.CharField(
        max_length=20, allow_blank=True, allow_null=True,
        validators=[RegexValidator(r'^\+\d{10,15}$')]
    )


class CustomerImageBaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = field_name in self.Meta.fields

    def validate(self, attrs):
        if not any(attrs.values()):
            raise serializers.ValidationError("An image is required.")
        return attrs

    class Meta:
        model = models.Customer
        fields = []


class CustomerIDFrontSerializer(CustomerImageBaseSerializer):
    id_image_front = serializers.ImageField(required=True)

    class Meta(CustomerImageBaseSerializer.Meta):
        fields = ["id_image_front"]


class CustomerIDBackSerializer(CustomerImageBaseSerializer):
    id_image_back = serializers.ImageField(required=True)

    class Meta(CustomerImageBaseSerializer.Meta):
        fields = ["id_image_back"]


class CustomerSelfieSerializer(CustomerImageBaseSerializer):
    selfie_image = serializers.ImageField(required=True)

    class Meta(CustomerImageBaseSerializer.Meta):
        fields = ["selfie_image"]


class CustomerProofAddressSerializer(CustomerImageBaseSerializer):
    address_proof_image = serializers.ImageField(required=True)

    class Meta(CustomerImageBaseSerializer.Meta):
        fields = ["address_proof_image"]


class CustomerVerificationSerializer(serializers.ModelSerializer):
    verification_status = serializers.ChoiceField(choices=CustomerStatus.CHOICES)
    customer_verified = serializers.BooleanField()
    remarks = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = models.Customer
        fields = ["verification_status", "customer_verified", "remarks"]


class CustomerSerializer(serializers.ModelSerializer):
    id_image_front_url = serializers.SerializerMethodField()
    id_image_back_url = serializers.SerializerMethodField()
    selfie_image_url = serializers.SerializerMethodField()
    address_proof_image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Customer
        fields = [
            "id", "user", "id_type", "id_number",
            "id_image_front_url", "id_image_back_url",
            "selfie_image_url", "address_proof_image_url",
            "verification_status", "customer_verified", "remarks",
            "created_at", "updated_at"
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.CharField(allow_null=True))
    def resolve_media_url(self, obj, field_name, alias):
        return ImageURLGenerator.build(obj, field_name, alias)

    def get_id_image_front_url(self, obj):
        return self.resolve_media_url(obj, "id_image_front", "front")

    def get_id_image_back_url(self, obj):
        return self.resolve_media_url(obj, "id_image_back", "back")

    def get_selfie_image_url(self, obj):
        return self.resolve_media_url(obj, "selfie_image", "selfie")

    def get_address_proof_image_url(self, obj):
        return self.resolve_media_url(obj, "address_proof_image", "address")


class CustomerAdminReviewSerializer(serializers.ModelSerializer):
    verification_status = serializers.ChoiceField(choices=CustomerStatus.CHOICES)
    remarks = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = models.Customer
        fields = ["verification_status", "remarks"]
