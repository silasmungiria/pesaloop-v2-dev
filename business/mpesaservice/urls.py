from django.urls import path
from .views import (
    STKPushView,
    STKCallbackView,
    C2BValidationView,
    C2BCallbackView,
)

urlpatterns = [
    path('stk-push/top-up/', STKPushView.as_view(), name='stk-push-top-up'),
    path('stk-push/callback/', STKCallbackView.as_view(), name='stk-push-callback'),

    path('paybill/validation/', C2BValidationView.as_view(), name='paybill-validation'),
    path('paybill/confirmation/callback/', C2BCallbackView.as_view(), name='paybill-confirmation-callback'),
]
