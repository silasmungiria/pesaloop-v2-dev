# RBAC Management Command Usage (PesaLoop)

This document provides usage instructions for the custom Django management commands defined under the RBAC module of the **PesaLoop** project.

These commands help maintain consistent role assignments and permission registration in your application.

---

## 📁 Structure

```

rbac/
└── management/
    ├── USAGE.md
    └── commands/
        ├── assign_default_roles.py
        └── register_permissions.py

```

---

## 📜 Commands

### 1. `assign_default_roles`

**File:** `rbac/management/commands/assign_default_roles.py`  
**Run:**

```bash
python manage.py assign_default_roles
```

**Purpose:**

Assigns the default role (marked `is_default=True`) to any user who does **not** already have an active role.

**Workflow:**

1. Retrieve the default role from the database.
2. Identify users without active `UserRole` assignments.
3. Use `RoleAssignmentService` to assign the default role to each.

**Sample Output:**

```
Assigned default role to 24 users.
```

**Error Case:**

```
No default role found.
```

---

### 2. `register_permissions`

**File:** `rbac/management/commands/register_permissions.py`
**Run:**

```bash
python manage.py register_permissions
```

**Purpose:**

Scans the project for all existing view-based permissions and registers them into the RBAC system.

**Workflow:**

1. Initializes RBAC via `RBACConfig.create('rbac')`.
2. Runs `register_existing_views()` to populate the permissions.

**Sample Output:**

```
Successfully registered all permissions
```

---

## ✅ When to Use

| Command                | Ideal Usage Scenarios                                      |
| ---------------------- | ---------------------------------------------------------- |
| `assign_default_roles` | After user imports, migrations, or fixing broken role data |
| `register_permissions` | After adding/modifying views requiring permissions         |

---

## 🧪 Verifying Execution

You can confirm successful execution by:

- Inspecting the `UserRole` table for new assignments.
- Checking the RBAC permission records.
- Re-running the command — it will skip already-assigned users/roles.

---

## 📄 Notes

- These commands are intended for internal project use.
- Integrate them into CI/CD or admin workflows as needed.
- They depend on proper setup of your models (`User`, `Role`, `UserRole`, etc.).

---

## 🤝 Contributing

Enhancements or bug fixes are welcome. Open a pull request or report issues directly in the PesaLoop project repository.

---
