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
    # except AttributeError:
    #     return None
    # except TypeError:
    #     return None


@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter
def splitlines(value):
    return value.splitlines()
