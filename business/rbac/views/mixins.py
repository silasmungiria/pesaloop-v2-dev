from rest_framework.response import Response

class PermissionViewMixin:
    """
    Mixin for views to handle permission checks
    """
    permission_required = None
    permission_denied_message = "You don't have permission to perform this action."
    
    def get_permission_required(self):
        method = self.request.method.upper()
        return getattr(self, f"{method}_permission", None) or self.permission_required

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.has_perm(self.get_permission_required()):
            self.permission_denied(
                request,
                message=self.permission_denied_message
            )

class AuditMixin:
    """
    Mixin for audit logging
    """
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        self.log_action(request, response)
        return response

    def log_action(self, request, response):
        # Only log actions for authenticated users
        if not request.user.is_authenticated:
            return

        from django.contrib.admin.models import LogEntry, CHANGE
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=None,
            object_id=None,
            object_repr=f"{self.__class__.__name__} action",
            action_flag=CHANGE,
            change_message=f"Performed {request.method} with status {response.status_code}"
        )
