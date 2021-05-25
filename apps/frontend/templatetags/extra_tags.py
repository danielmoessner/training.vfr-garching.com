import urllib.parse

from django.http import HttpRequest
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return None


@register.filter
def get_item2(data, key):
    if not data:
        return None
    # try:
    keys = key.split('.')
    try:
        data = data[keys[0]]
    except TypeError:
        data = getattr(data, keys[0])
    if len(keys) == 1:
        return data
    else:
        return get_item2(data, '.'.join(keys[1:]))


@register.filter
def to_int(value):
    return int(value)


@register.filter
def default2(value, arg):
    return value or arg or None


@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter
def splitlines(value):
    return value.splitlines()


@register.filter
def filter_show_on_detail(filters_qs):
    filters = list(filters_qs)
    filters = list(filter(lambda f: f.show_on_detail, filters))
    return filters


@register.inclusion_tag('symbols/request/params.html', takes_context=True)
def url_params(context):
    request = context['request']
    get_params = []
    for key, value in request.GET.items():
        get_params.append('{}={}'.format(key, urllib.parse.quote(value)))
    get_params = '&'.join(get_params)
    return {"get_params": get_params}
