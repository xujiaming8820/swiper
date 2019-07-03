from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from common import utils, errors
from lib.http import render_json
from user import logic


def verify_phone(request):
    """
    验证手机号
    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num')

    if utils.is_phone_num(phone_num.strip()):
        # 生成随机验证码
        # 发送随机验证码
        logic.send_verify_code(phone_num)
        return render_json()

    return render_json(code=errors.PHONE_NUM_ERR)
