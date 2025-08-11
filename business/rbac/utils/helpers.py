def get_permission_string(codename, method='ALL'):
    """
    Format permission string for checking
    """
    return f"{codename}.{method}" if method != 'ALL' else f"{codename}.ALL"

def check_permission(user, codename, method='ALL'):
    """
    Helper function to check permissions in views or templates
    """
    if user.is_superuser:
        return True
    perm_string = get_permission_string(codename, method)
    return perm_string in user.get_all_permissions()
