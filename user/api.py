from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from common import utils, errors
from lib.http import render_json
from lib.sms import send
from user import logic
from user.models import User


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
        if logic.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SMS_SEND_ERR)

    return render_json(code=errors.PHONE_NUM_ERR)


def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num')
    code = request.POST.get('code')

    print(phone_num, code)
    user = User.objects.filter(phonenum=phone_num).first()
    if user:
        data = {
            'uid': user.id,
            'nickname': user.nickname,
            'age': datetime.now().year - user.birth_year,
            'sex': user.sex,
            'location': user.location,
            'avatars': user.avatar
        }
        print(data)
        return render_json({'code': 200, 'data': data})
    else:
        print(2222)
    # user = User.objects.filter(phone_num=phone_num)
    # print(user)

    return JsonResponse({'code': 200})
