from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PermissionViewSet,
    RoleViewSet,
    UserRoleViewSet,
    RolePermissionViewSet
)

router = DefaultRouter()
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'user-roles', UserRoleViewSet, basename='userrole')
router.register(r'role-permissions', RolePermissionViewSet, basename='rolepermission')

urlpatterns = [
    path('', include(router.urls)),
]
