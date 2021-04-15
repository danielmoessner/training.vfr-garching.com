from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter
def splitlines(value):
    return value.splitlines()
