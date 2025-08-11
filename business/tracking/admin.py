from django.contrib import admin
from django.utils.html import format_html
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('type', 'user_email', 'ip_address', 'endpoint_short', 'timestamp', 'flagged_display')
    list_filter = ('type', 'flagged', 'country', 'method')
    search_fields = ('user__email', 'ip_address', 'endpoint', 'city', 'country')
    readonly_fields = ('timestamp', 'location_display', 'device_summary_display')
    list_per_page = 50
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Core Metadata', {
            'fields': ('type', 'timestamp', 'flagged', 'tags')
        }),
        ('User Context', {
            'fields': ('user', 'session_id')
        }),
        ('Request Context', {
            'fields': ('endpoint', 'method', 'status', 'duration', 'referrer')
        }),
        ('Network Context', {
            'fields': ('ip_address', 'is_routable')
        }),
        ('Geo Context', {
            'fields': ('location_display', 'country', 'region', 'city', 'coordinates')
        }),
        ('Device Context', {
            'fields': ('device_summary_display', 'user_agent')
        }),
    )

    def user_email(self, obj):
        return obj.user.email if obj.user else ''
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'

    def endpoint_short(self, obj):
        return obj.endpoint[:50] + '...' if len(obj.endpoint) > 50 else obj.endpoint
    endpoint_short.short_description = 'Endpoint'

    def flagged_display(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if obj.flagged else 'green',
            '⚠️ Flagged' if obj.flagged else '✓ Normal'
        )
    flagged_display.short_description = 'Status'

    def location_display(self, obj):
        return obj.location
    location_display.short_description = 'Location'

    def device_summary_display(self, obj):
        return obj.device_summary
    device_summary_display.short_description = 'Device Summary'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
