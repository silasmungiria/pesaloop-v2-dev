from rest_framework import serializers
from ..models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    user_email = serializers.SerializerMethodField()
    location = serializers.CharField(read_only=True)
    device_summary = serializers.CharField(read_only=True)
    duration_ms = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('id', 'timestamp')
        extra_kwargs = {
            'ip_address': {'required': True},
            'endpoint': {'required': True},
            'method': {'required': True},
            'params': {'required': False, 'allow_null': False, 'default': dict},
            'headers': {'required': False, 'allow_null': False, 'default': dict},
        }

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None

    def get_duration_ms(self, obj):
        return round(obj.duration * 1000, 2) if obj.duration else None

    def validate(self, data):
        if 'ip_address' in data and not data['ip_address']:
            raise serializers.ValidationError({'ip_address': 'IP address cannot be empty'})
        return data

    def validate_params(self, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            try:
                return dict(value)
            except (TypeError, ValueError):
                return {}
        return value

class ActivityListSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    user_email = serializers.SerializerMethodField()
    location = serializers.CharField(read_only=True)
    device_summary = serializers.CharField(read_only=True)

    class Meta:
        model = Activity
        fields = (
            'id', 'timestamp', 'type', 'type_display', 'flagged',
            'user', 'user_email', 'ip_address', 'endpoint',
            'method', 'status', 'duration', 'country', 'location',
            'device_summary'
        )

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None


class ActivityFlagResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    flagged = serializers.BooleanField()
    message = serializers.CharField()


from rest_framework import serializers
from tracking.models import Activity
from tracking.utils import ActivityType

class CountStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    flagged = serializers.IntegerField()
    last_30_days = serializers.IntegerField()

class ResponseTimeStatsSerializer(serializers.Serializer):
    avg = serializers.FloatField(required=False, allow_null=True)
    max = serializers.FloatField(required=False, allow_null=True)
    min = serializers.FloatField(required=False, allow_null=True)

class ActivityTypeStatsSerializer(serializers.Serializer):
    type = serializers.CharField()
    type_display = serializers.SerializerMethodField()
    count = serializers.IntegerField()

    def get_type_display(self, obj):
        return dict(ActivityType.choices).get(obj['type'], obj['type'])

class EndpointStatsSerializer(serializers.Serializer):
    endpoint = serializers.CharField()
    method = serializers.CharField()
    count = serializers.IntegerField()
    avg_time = serializers.FloatField(required=False, allow_null=True)
    errors = serializers.IntegerField()

class GeographyStatsSerializer(serializers.Serializer):
    country = serializers.CharField()
    count = serializers.IntegerField()

class DeviceStatsSerializer(serializers.Serializer):
    device = serializers.CharField()
    os = serializers.CharField()
    browser = serializers.CharField()
    count = serializers.IntegerField()

class UserStatsSerializer(serializers.Serializer):
    email = serializers.EmailField(source='user__email')
    count = serializers.IntegerField()

class ActivityStatsSerializer(serializers.Serializer):
    counts = CountStatsSerializer()
    response_times = ResponseTimeStatsSerializer()
    types = ActivityTypeStatsSerializer(many=True)
    endpoints = EndpointStatsSerializer(many=True)
    geography = GeographyStatsSerializer(many=True)
    devices = DeviceStatsSerializer(many=True)
    users = UserStatsSerializer(many=True)

