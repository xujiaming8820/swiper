import logging
import os
import time
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

from common import utils, errors, config
from libs.http import render_json
from user import logic
from user.forms import ProfileForm
from user.models import User, Profile

logger = logging.getLogger('inf')


def verify_phone(request):
    """
    验证手机号
    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num', '')
    phone_num = phone_num.strip()

    if utils.is_phone_num(phone_num):
        if logic.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SmsSendError.code)

    return render_json(code=errors.PhoneNumError.code)


def login(request):
    phone_num = request.POST.get('phone_num', '')
    code = request.POST.get('code', '')

    phone_num = phone_num.strip()
    code = code.strip()

    # 1、检查 验证码
    cached_code = cache.get(config.VERIFY_CODE_CACHE_PREFIX % phone_num)
    if cached_code != code:
        return render_json(code=errors.VerifyCodeError.code)

    # 2、登录或注册
    # try:
    #     user = User.get(phonenum=phone)
    # except User.DoesNotExist:
    #     user = User.objects.create(phonenum=phone)
    #     # 创建用户的同时，使用 user.id 创建 Profile 对象，建立一对一的关联
    #     Profile.objects.create(id=user.id)

    user, created = User.get_or_create(phonenum=phone_num)
    request.session['uid'] = user.id

    logger.info('user.login, uid:%s' % user.id)

    return render_json(data=user.to_dict())


def get_profile(request):
    user = request.user

    # 1、先从缓存中获取 profile_data
    key = config.PROFILE_DATA_CACHE_PREFIX % user.id
    profile_data = cache.get(key)
    logger.debug('get from cache')
    print('get from cache')

    # 2、如果缓存中没有，则从数据库获取
    if profile_data is None:
        profile = user.profile
        profile_data = profile.to_dict(exclude=['vibration', 'only_matche', 'auto_play'])
        logger.debug('get from DB')

        # 3、将 profile_data 存储至缓存
        cache.set(key, profile_data)
        logger.debug('set cache')

    return render_json(data=profile_data)


def set_profile(request):
    user = request.user

    form = ProfileForm(request.POST, instance=user.profile)

    if form.is_valid():
        profile = form.save()

        # 保存成功后，直接更新缓存
        # 也可以通过直接删除缓存的方式更新缓存内容
        key = config.PROFILE_DATA_CACHE_PREFIX % user.id
        profile_data = profile.to_dict(exclude=['vibration', 'only_matche', 'auto_play'])
        cache.set(key, profile_data)

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
        return render_json(code=errors.AvatarUploadError.code)
