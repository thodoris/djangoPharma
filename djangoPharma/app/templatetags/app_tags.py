from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except:
        return False  # group doesn't exist, so for sure the user isn't part of the group

    # for superuser , always return True
    if user.is_superuser:
        return True

    return user.groups.filter(name=group_name).exists()


# The first argument *must* be called "context" here.
def breadcrumb_tag(context):
    request = context['request']
    address = request.path
    return {
        'link':address,
        'title': address,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/breadcrumb.html', takes_context=True)(breadcrumb_tag)