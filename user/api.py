import os
import time
from datetime import datetime

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from common import utils, errors, config
from libs.http import render_json
from libs.sms import send
from swiper import settings
from user import logic
from user.forms import ProfileForm
from user.models import User, Profile


def verify_phone(request):
    """
    验证手机号
    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num', '')
    phone_num = phone_num.strip()

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
    phone_num = request.POST.get('phone_num', '')
    code = request.POST.get('code', '')

    phone_num = phone_num.strip()
    code = code.strip()

    # 1.检查验证码
    cached_code = cache.get(config.VERIFY_CODE_CACHE_PREFIX % phone_num)
    if cached_code != code:
        return render_json(code=errors.VERIFY_CODE_ERR)

    # 2.登录或注册
    user, created = User.objects.get_or_create(phonenum=phone_num)
    request.session['uid'] = user.id

    return render_json(data=user.to_dict())


def get_profile(request):
    """
    获取查找信息
    :param request:
    :return:
    """
    profile = request.user.profile
    return render_json(data=profile.to_dict(exclude=['vibration', 'only_matche', 'auto_play']))


def set_profile(request):
    """
    更新查找信息
    :param request:
    :return:
    """
    user = request.user

    form = ProfileForm(request.POST, instance=user.profile)

    if form.is_valid():
        form.save()
        return render_json()
    else:
        return render_json(data=form.errors)


def upload_avatar(request):
    avatar = request.FILES.get('avatar')
    user = request.user

    # filename = 'avatar-%s-%d' % (user.id, int(time.time()))
    # filepath = os.path.join(settings.MEDIA_ROOT, filename)
    #
    # with open(filepath, 'wb+') as output:
    #     for chunk in avatar.chunks():
    #         output.write(chunk)

    ret = logic.async_upload_avatar(user, avatar)

    if ret:
        return render_json()
    else:
        return render_json(code=errors.AVATAR_UPLOAD_ERR)
