# permissions.py for store app

from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

buyer = {
    'can_view_products': True,
    'can_create_orders': True,
    'can_edit_profile': True,
    'can_view_suppliers': False,
    'can_manage_deliveries': False,
    # Add more permissions as needed
}

supplier = {
    'can_view_products': True,
    'can_create_products': True,
    'can_edit_products': True,
    'can_view_buyers': False,
    'can_manage_orders': True,
    # Add more permissions as needed
}

admin = {
    'can_view_all': True,
    'can_edit_all': True,
    'can_delete': True,
    'can_manage_users': True,
    # Add more permissions as needed
}

def has_permission(role, permission):
    """
    Helper function to check if a role has a specific permission.
    Admins have access to all permissions automatically.
    """
    if role == 'admin':
        return True
    perms = globals().get(role, {})
    return perms.get(permission, False)

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            # Superusers (admins) have full access automatically
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            for role in roles:
                if role == 'buyer' and request.user.is_buyer:
                    return view_func(request, *args, **kwargs)
                if role == 'supplier' and request.user.is_supplier:
                    return view_func(request, *args, **kwargs)
                if role == 'admin' and request.user.is_admin:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator