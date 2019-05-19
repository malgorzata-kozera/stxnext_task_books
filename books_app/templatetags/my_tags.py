from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Fixing pagination.
    Return URL parameters that are the same as the current
    request's parameters.
    It also removes any empty parameters.
    """
    d = context['request'].GET.copy()

    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
