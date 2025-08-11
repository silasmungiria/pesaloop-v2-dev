import logging
from functools import wraps

from celery import shared_task
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from ipware import get_client_ip

from tracking.utils import ActivityType
from .tracker import ActivityTracker

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def track_activity_async(
    self,
    user_id=None,
    request_path=None,
    request_method=None,
    activity_type=None,
    status_code=None,
    sensitive_fields=None,
    user_agent=None,
    ip_address=None,
    request_data=None,
):
    """
    Background task to track activity asynchronously.
    """
    try:
        request = HttpRequest()
        request.method = request_method
        request.path = request_path
        request.META = {
            "HTTP_USER_AGENT": user_agent or "",
            "REMOTE_ADDR": ip_address or "0.0.0.0",
        }
        request.data = request_data or {}

        if user_id:
            try:
                request.user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                request.user = None

        response = HttpResponse(status=status_code or 200)
        response.headers["X-Response-Time"] = "0.1"

        tracker = ActivityTracker(request, response, sensitive_fields)
        tracker.capture(activity_type=activity_type)

    except Exception as exc:
        logger.error("Async tracking failed: %s", str(exc), exc_info=True)
        raise self.retry(exc=exc)


def track_activity(activity_type=ActivityType.OTHER, async_mode=False, sensitive_fields=None):
    """
    Decorator to track view activity (sync or async).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_or_request, *args, **kwargs):
            request = view_or_request if hasattr(view_or_request, "META") else view_or_request.request
            ip, _ = get_client_ip(request)
            ip_address = ip or "0.0.0.0"

            response = None
            try:
                response = view_func(view_or_request, *args, **kwargs)

                if async_mode:
                    track_activity_async.delay(
                        user_id=getattr(request.user, "id", None),
                        request_path=request.path,
                        request_method=request.method,
                        activity_type=activity_type,
                        status_code=getattr(response, "status_code", None),
                        sensitive_fields=sensitive_fields,
                        user_agent=request.META.get("HTTP_USER_AGENT", ""),
                        ip_address=ip_address,
                        request_data=getattr(request, "data", None),
                    )
                else:
                    tracker = ActivityTracker(request, response, sensitive_fields)
                    tracker.capture(activity_type=activity_type)

                return response

            except Exception as e:
                logger.error("Activity tracking failed: %s", str(e), exc_info=True)
                if response is None:
                    raise
                return response

        return _wrapped_view

    return decorator
