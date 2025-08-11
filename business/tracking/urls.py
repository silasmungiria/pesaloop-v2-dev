from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ActivityListView,
    ActivityDetailView,
    ActivityDeleteView,
    ActivityStatsView,
    ActivityExportView,
)

router = DefaultRouter()
router.register(r'activities/export', ActivityExportView, basename='activity-export')

urlpatterns = [
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('activities/<uuid:id>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('activities/<uuid:id>/delete/', ActivityDeleteView.as_view(), name='activity-delete'),
    path('activities/stats/', ActivityStatsView.as_view(), name='activity-stats'),
]

urlpatterns += router.urls
