
# def send(phone_num, code):
#     print('sms.send', phone_num, code)
#     return code
import requests
from django.conf import settings

from common import config


def send(phone_num, code):
    if settings.DEBUG:
        print(phone_num, code)
        return True

    params = config.YZX_SMS_PARAMS.copy()
    params['mobile'] = phone_num
    params['param'] = code

    resp = requests.post(config.YZX_SMS_URL, json=params)

    if resp.status_code == 200:
        result = resp.json()
        if result.get('code') == "000000":
            return True

    return False
