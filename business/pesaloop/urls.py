import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # ----------------------------------------
    # Core & Admin
    # ----------------------------------------
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    # ----------------------------------------
    # API Documentation
    # ----------------------------------------
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='openapi-schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='openapi-schema'), name='redoc-ui'),

    # ----------------------------------------
    # Authentication & User Management
    # ----------------------------------------
    path('api/auth/', include('authservice.urls')),
    path('api/users/', include('userservice.urls')),

    # ----------------------------------------
    # Role-Based Access Control (RBAC)
    # ----------------------------------------
    path('api/rbac/', include('rbac.urls')),

    # ----------------------------------------
    # Financial Services
    # ----------------------------------------
    path('api/wallets/', include('walletservice.urls')),
    path('api/payments/', include('paymentservice.urls')),
    path('api/credits/', include('creditservice.urls')),
    path('api/forex/', include('forexservice.urls')),

    # ----------------------------------------
    # Integrations
    # ----------------------------------------
    path('api/mpesaservice/', include('mpesaservice.urls')),
    # path('api/cardservice/', include('cardservice.urls')),

    # ----------------------------------------
    # Media & Content
    # ----------------------------------------
    path('api/media/', include('mediaservice.urls')),

    # ----------------------------------------
    # Monitoring & Reporting
    # ----------------------------------------
    path('api/reports/', include('reportingservice.urls')),
    # path('api/audit/', include('easyaudit.urls')),
    path('api/tracking/', include('tracking.urls')),
]
