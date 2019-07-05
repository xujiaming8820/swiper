from django.conf import settings
from django.http import JsonResponse

from common import errors


def render_json(code=errors.OK, data=None):
    """
    自定义 json 输出
    :param code:
    :param data:
    :return:
    """

    result = {
        'code': code
    }

    if data:
        result['data'] = data

    if settings.DEBUG:
        json_dumps_params = {'indent': 4, 'ensure_ascii': False}
    else:
        json_dumps_params = {'separators': (',', ':')}

    return JsonResponse(result, safe=False, json_dumps_params=json_dumps_params)
