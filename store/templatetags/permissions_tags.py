from django import template
from ..permissions import has_permission

register = template.Library()

@register.simple_tag(takes_context=True)
def has_perm(context, permission):
    user = context['user']
    role = user.role if user.is_authenticated else None
    if role:
        return has_permission(role, permission)
    return False