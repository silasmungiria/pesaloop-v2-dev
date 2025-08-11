# Django Advanced RBAC (Role-Based Access Control) System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-3.2%2B-green)
![DRF](https://img.shields.io/badge/djangorestframework-3.12%2B-red)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Permission System](#-permission-system)
- [Role Hierarchy](#-role-hierarchy)
- [Advanced Features](#-advanced-features)
- [Performance Optimization](#-performance-optimization)
- [Security Considerations](#-security-considerations)
- [Testing Strategy](#-testing-strategy)
- [Troubleshooting](#-troubleshooting)
- [FAQs](#-faqs)
- [Contributing](#-contributing)
- [License](#-license)

## 🌐 Overview

This Django application provides a comprehensive Role-Based Access Control (RBAC) system designed to replace Django's built-in permissions and groups with a more sophisticated, hierarchical permission management solution. The system is particularly suited for:

- Enterprise applications requiring granular access control
- Financial systems needing audit trails
- Healthcare applications with strict access requirements
- SaaS platforms with multi-tenant authorization needs

The RBAC system extends Django's authentication framework while maintaining compatibility with existing Django and Django REST Framework components.

## ✨ Key Features

### Core Functionality

- **Hierarchical Role System**: Five distinct role levels with increasing privileges
- **Method-Specific Permissions**: Granular control over HTTP methods (GET, POST, PUT, etc.)
- **Automatic Permission Discovery**: Auto-registers permissions from views and models
- **Default Role Assignment**: Ensures all users have at least basic access
- **Time-Based Restrictions**: Limit access to specific days/hours
- **Sensitive Operation Protection**: Require additional authentication for critical actions

### Advanced Capabilities

- **Permission Caching**: Redis-backed caching with configurable TTL
- **Audit Logging**: Comprehensive tracking of all access attempts
- **Bulk Operations**: Efficient role cloning and mass assignment
- **Expirable Roles**: Temporary access grants with automatic revocation
- **View Decorators**: Simplified permission checks for function-based views
- **Admin Integration**: Full CRUD support in Django Admin

### Integration Features

- **DRF ViewSet Support**: Seamless integration with Django REST Framework
- **Custom User Model Support**: Works with any AUTH_USER_MODEL
- **Management Commands**: Utility commands for system maintenance
- **Signal Handlers**: Automatic system configuration hooks

## 🏛 Architecture

The system follows a layered architecture:

```
┌───────────────────────────────────────────────────┐
│                   Django Project                  │
└───────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────┐
│                    RBAC App                       │
├─────────────────┬─────────────────┬───────────────┤
│   Models Layer  │  Services Layer │   API Layer   │
└─────────────────┴─────────────────┴───────────────┘
```

### Component Breakdown

1. **Models**:

   - `Role`: Defines access levels and default status
   - `Permission`: Stores granular access rules
   - `RolePermission`: Many-to-many relationship between roles and permissions
   - `UserRole`: Assigns roles to users with expiration tracking

2. **Services**:

   - `RoleAssignmentService`: Handles role assignment logic
   - `PermissionRegistry`: Auto-discovers and registers permissions
   - `PermissionCache`: Manages permission caching layer

3. **API**:
   - RESTful endpoints for all RBAC operations
   - Swagger/OpenAPI documentation
   - Custom permission classes for DRF

## 🛠 Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+

### Installation Steps

1. Install the package:

```bash
pip install git+https://github.com/your-repo/rbac.git
```

2. Add to your Django project:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rbac',
]
```

3. Configure the database:

```bash
python manage.py makemigrations rbac
python manage.py migrate
```

4. Set up default permissions:

```bash
python manage.py register_permissions
```

## ⚙ Configuration

### Required Settings

```python
# settings.py
AUTH_USER_MODEL = 'users.CustomUser'  # Your custom user model
```

### Recommended Settings

```python
# RBAC-specific configurations
RBAC = {
    'CACHE_TIMEOUT': 300,  # 5 minutes
    'DEFAULT_ROLE_NAME': 'Basic User',
    'BUSINESS_HOURS': {
        'ENABLED': True,
        'START_HOUR': 9,  # 9 AM
        'END_HOUR': 17,   # 5 PM
        'TIMEZONE': 'UTC',
    },
    'SENSITIVE_METHODS': ['DELETE', 'PATCH'],
}
```

### DRF Integration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rbac.permissions.MethodPermission',
        'rbac.permissions.SensitiveOperationPermission',
        'rbac.permissions.BusinessHoursAccessPermission',
    ],
}
```

## 📚 Usage Guide

### 1. Basic Setup

**Create Initial Roles:**

```python
from rbac.models import Role

basic_role = Role.objects.create(
    name="Basic User",
    level=1,
    is_default=True,
    description="Default access level for all users"
)

admin_role = Role.objects.create(
    name="Administrator",
    level=4,
    is_default=False,
    description="Full system access"
)
```

**Register Model Permissions:**

```python
from django.db import models
from rbac.models import Permission

class Account(models.Model):
    class Meta:
        permission_basename = 'account'

    # Model fields...
```

### 2. Protecting Views

**Class-Based Views:**

```python
from rbac.permissions import register_permissions
from rest_framework.viewsets import ModelViewSet

@register_permissions
class TransactionViewSet(ModelViewSet):
    """
    Requires:
    - view_transactions for GET
    - create_transactions for POST
    - change_transactions for PUT/PATCH
    - delete_transactions for DELETE
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # Method-specific permissions
    get_permission = 'view_transactions'
    post_permission = 'create_transactions'
    put_permission = 'change_transactions'
    patch_permission = 'change_transactions'
    delete_permission = 'delete_transactions'

    # Additional requirements
    required_permission = 'financial_access'
```

**Function-Based Views:**

```python
from rbac.permissions import permission_required
from django.http import JsonResponse

@permission_required('approve_loan', method='POST')
def approve_loan(request, loan_id):
    """
    Requires approve_loan permission for POST method
    """
    try:
        # Business logic here
        return JsonResponse({'status': 'approved'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
```

### 3. Managing Access

**Assign Roles:**

```python
from rbac.services import RoleAssignmentService

def promote_to_admin(user, promoted_by):
    admin_role = Role.objects.get(name="Administrator")
    try:
        RoleAssignmentService.assign_role(
            user=user,
            role=admin_role,
            assigned_by=promoted_by,
            expires_at=None,  # Permanent role
            notes="Promoted to administrator"
        )
        return True
    except PermissionDenied as e:
        logger.error(f"Role assignment failed: {str(e)}")
        return False
```

**Check Permissions:**

```python
# In views/templates
if request.user.has_perm('delete_users', 'DELETE'):
    # Show delete button
    pass

# In business logic
from rbac.utils import check_permission

def transfer_funds(user, amount):
    if not check_permission(user, 'perform_transfers', 'POST'):
        raise PermissionError("Insufficient permissions")

    if amount > 10000 and not check_permission(user, 'large_transfers', 'POST'):
        raise PermissionError("Additional permissions required for large transfers")

    # Process transfer
```

## 📡 API Documentation

The RBAC system provides these RESTful endpoints:

### Permissions

- `GET /api/rbac/permissions/` - List all permissions
- `POST /api/rbac/permissions/` - Create new permission
- `GET /api/rbac/permissions/{id}/` - Retrieve permission details
- `PUT /api/rbac/permissions/{id}/` - Update permission
- `DELETE /api/rbac/permissions/{id}/` - Delete permission

### Roles

- `GET /api/rbac/roles/` - List all roles
- `POST /api/rbac/roles/` - Create new role
- `GET /api/rbac/roles/{id}/` - Retrieve role details
- `PUT /api/rbac/roles/{id}/` - Update role
- `DELETE /api/rbac/roles/{id}/` - Delete role
- `POST /api/rbac/roles/{id}/clone/` - Clone role with permissions

### User Roles

- `GET /api/rbac/user-roles/` - List all user-role assignments
- `POST /api/rbac/user-roles/` - Assign role to user
- `GET /api/rbac/user-roles/{id}/` - Retrieve assignment details
- `PUT /api/rbac/user-roles/{id}/` - Update assignment
- `DELETE /api/rbac/user-roles/{id}/` - Revoke role
- `POST /api/rbac/user-roles/{id}/activate/` - Activate inactive role
- `POST /api/rbac/user-roles/{id}/deactivate/` - Deactivate role

All endpoints support:

- Filtering by related objects
- Pagination
- Search
- Ordering

Example request:

```bash
curl -X GET \
  'http://localhost:8000/api/rbac/roles/?level__gte=3&ordering=name' \
  -H 'Authorization: Token xxxxx'
```

## 🔐 Permission System

### Permission Structure

Permissions follow this format:

```
<action>_<resource>.<method>

Examples:
- view_dashboard.GET
- create_user.POST
- update_account.PUT
- delete_transaction.DELETE
- manage_settings.ALL
```

### Permission Categories

1. **User Management** (USER)
2. **Financial Transactions** (TRANSACTION)
3. **Loan Operations** (LOAN)
4. **Reporting** (REPORT)
5. **System Administration** (SYSTEM)

### Special Permissions

- `*.ALL`: Grants access for all methods
- `sensitive.*`: Requires biometric authentication
- `after_hours.*`: Bypasses time restrictions

## 👑 Role Hierarchy

The system implements a strict role hierarchy:

| Level | Name          | Description                    | Example Roles       |
| ----- | ------------- | ------------------------------ | ------------------- |
| 1     | Basic         | Read-only access               | Guest, Viewer       |
| 2     | Intermediate  | Basic create/update operations | Editor, Contributor |
| 3     | Senior        | Advanced operations            | Manager, Analyst    |
| 4     | Administrator | Sensitive system operations    | Admin, Director     |
| 5     | System        | Bypasses all restrictions      | Superuser, System   |

Key rules:

- Users can only assign roles at lower levels
- Permission checks respect level hierarchy
- System-level roles ignore all restrictions

## 🚀 Advanced Features

### 1. Biometric Protection

```python
from rbac.permissions import SensitiveOperationPermission

class PaymentViewSet(ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        MethodPermission,
        SensitiveOperationPermission
    ]
    sensitive_methods = ['POST', 'DELETE']
```

### 2. Business Hours Restriction

```python
# settings.py
RBAC_BUSINESS_HOURS = {
    'ENABLED': True,
    'START_HOUR': 8,
    'END_HOUR': 18,
    'TIMEZONE': 'America/New_York',
    'BYPASS_PERMISSION': 'after_hours_access'
}
```

### 3. Permission Inheritance

```python
# Parent role gets all permissions of child roles
def get_effective_permissions(role):
    child_roles = Role.objects.filter(level__lt=role.level)
    return Permission.objects.filter(
        role_permissions__role__in=child_roles
    ).distinct()
```

### 4. Audit Logging

```python
# settings.py
LOGGING = {
    'loggers': {
        'rbac.audit': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
```

## ⚡ Performance Optimization

### Caching Strategy

```python
# settings.py
CACHES = {
    'rbac': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 300  # 5 minutes
    }
}

RBAC_CACHE_ALIAS = 'rbac'
```

### Query Optimization

```python
# Always use select_related/prefetch_related
UserRole.objects.filter(user=user)\
    .select_related('role')\
    .prefetch_related('role__permissions__permission')\
    .filter(is_active=True)
```

### Bulk Operations

```python
from rbac.services import bulk_assign_roles

def onboard_users(users, role):
    results = bulk_assign_roles(
        users=users,
        role=role,
        assigned_by=system_user
    )
    success_count = sum(1 for r in results if r['success'])
```

## 🔒 Security Considerations

### 1. Principle of Least Privilege

- Always start with minimal permissions
- Grant additional access only when required
- Regularly audit role assignments

### 2. Sensitive Operations

- Mark financial/delete operations as sensitive
- Implement two-factor authentication
- Maintain detailed audit logs

### 3. Session Security

- Implement session timeout
- Invalidate permissions cache on logout
- Monitor for suspicious activity

### 4. Regular Audits

```bash
# Generate permission report
python manage.py dumpdata rbac.Permission --indent 2 > permissions.json

# Audit user roles
python manage.py shell -c "
from rbac.models import UserRole
from datetime import date
print(UserRole.objects.filter(expires_at__lt=date.today(), is_active=True).count())
"
```

## 🧪 Testing Strategy

### Unit Tests

```python
from rbac.test_utils import RBACTestCase

class PermissionTests(RBACTestCase):
    def setUp(self):
        self.basic_user = self.create_user(role_level=1)
        self.admin_user = self.create_user(role_level=4)

    def test_basic_user_access(self):
        self.client.force_login(self.basic_user)
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 403)

    def test_admin_access(self):
        self.client.force_login(self.admin_user)
        response = self.client.post('/api/users/', data={...})
        self.assertEqual(response.status_code, 201)
```

### Integration Tests

```python
class BusinessHoursTest(TestCase):
    @override_settings(RBAC_BUSINESS_HOURS={'ENABLED': True, 'START_HOUR': 9, 'END_HOUR': 17})
    def test_after_hours_access(self):
        with self.mock_time(hour=18):  # 6 PM
            user = self.create_user_with_permission('after_hours_access')
            self.client.force_login(user)
            response = self.client.get('/api/reports/')
            self.assertEqual(response.status_code, 200)
```

### Load Testing

```python
# tests/load/test_permission_cache.py
class PermissionCacheLoadTest(LoadTestBase):
    USERS = 100
    ITERATIONS = 1000

    def test_permission_check_performance(self):
        results = self.run_load_test(
            operation=lambda: self.user.has_perm('view_reports'),
            iterations=self.ITERATIONS
        )
        self.assertLess(results['avg_time'], 0.01)  # 10ms
```

## 🚨 Troubleshooting

### Common Issues

**Permissions Not Registering**

1. Verify `@register_permissions` decorator is applied
2. Check `register_permissions` command output
3. Confirm view has `permission_classes` set

**Role Assignment Failing**

1. Check assigner's role level meets requirement
2. Verify target user doesn't already have the role
3. Confirm role isn't expired

**Cache Inconsistencies**

1. Manually clear cache: `python manage.py clear_rbac_cache`
2. Verify Redis connection
3. Check cache timeout settings

### Debugging Tips

```python
# Debug permission checks
from rbac.utils import debug_permissions

def some_view(request):
    debug_permissions(request.user)
    # Outputs all permissions to console
```

## ❓ FAQs

**Q: How do I migrate from Django's built-in permissions?**
A: Use the included migration script:

```bash
python manage.py migrate_django_permissions
```

**Q: Can I use this with GraphQL?**
A: Yes, integrate the permission checks in your GraphQL resolvers:

```python
def resolve_protected_field(self, info):
    if not info.context.user.has_perm('view_protected'):
        return None
    return sensitive_data
```

**Q: How to handle permission changes in production?**

1. Deploy changes
2. Run `register_permissions`
3. Clear permission cache
4. Notify users of changes

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add some feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

### Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
pre-commit install
```

### Testing

```bash
pytest tests/ --cov=rbac --cov-report=html
```

## 📜 License

MIT License

Copyright (c) 2025 Silas Mugambi

Permission is hereby granted...

---
