from django import template

register = template.Library()

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