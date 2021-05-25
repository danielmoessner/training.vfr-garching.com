import urllib.parse


def get_params_from_request(request):
    get_params = []
    for key, value in request.GET.items():
        get_params.append('{}={}'.format(key, urllib.parse.quote(value)))
    get_params = '&'.join(get_params)
    return get_params
