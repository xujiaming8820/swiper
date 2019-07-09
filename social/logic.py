import datetime

from django.core.cache import cache

from common import errors, config
from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    """
    筛选符合 user.profile 条件的用户
    过滤掉已经被划过的用户
    :param user:
    :return:
    """
    today = datetime.date.today()

    # 1999 = 2019 - 20
    max_year = today.year - user.profile.min_dating_age
    # 2001 = 2019 - 18
    min_year = today.year - user.profile.max_dating_age

    swiped_users = Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list = [s.sid for s in swiped_users]

    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__gte=min_year,
        birth_year__lte=max_year,
    ).exclude(id__in=swiped_sid_list)[:20]

    return users


def like_someone(uid, sid):
    """
    创建喜欢的人，如果对方也喜欢，则建立好友关系
    :param uid:
    :param sid:
    :return:
    """
    if not User.objects.filter(id=sid).exists():
        raise errors.SidError

    # 创建滑动记录
    ret = Swiped.swipe(uid=uid, sid=sid, mark='like')

    # 只有滑动成功，才可以进行好友匹配操作
    # 如果被滑动人喜欢过我，则建立好友关系
    if ret and Swiped.is_liked(sid, uid):
        # Friend.make_friends(uid, sid)
        # TODO 向 sid 用户推送通知
        Friend.objects.make_friends(uid, sid)

    return ret


def superlike_someone(uid, sid):
    """
    创建超级喜欢的人，如果对方也喜欢，则建立好友关系
    :param uid:
    :param sid:
    :return:
    """
    if not User.objects.filter(id=sid).exists():
        raise errors.SidError

        # 创建滑动记录
    ret = Swiped.swipe(uid=uid, sid=sid, mark='superlike')

    # 只有滑动成功，才可以进行好友匹配操作
    # 如果被滑动人喜欢过我，则建立好友关系
    if ret and Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True

    return False


def rewind(user):
    """
    撤销当前用户登录的上一次滑动操作
    每天只能撤销3次
    :param user:
    :return:
    """
    key = config.REWIND_CACHE_PREFIX % user.id

    rewind_times = cache.get(key, 0)

    if rewind_times >= config.REWIND_TIMES:
        raise errors.RewindLimitError

    swipe = Swiped.objects.filter(uid=user.id).latest('created_at')

    if swipe.mark in ['like', 'superlike']:
        Friend.cancel_friends(user.id, swipe.sid)

    swipe.delete()

    now = datetime.datetime.now()
    timeout = 86400 - now.hour * 3600 - now.minute * 60 - now.second

    cache.set(key, rewind_times + 1, timeout=timeout)


def liked_me(user):
    """
    喜欢我的人列表
    :param user:
    :return:
    """

    friend_uid_list = Friend.friend_list(user.id)

    swipe_list = Swiped.objects.filter(sid=user.id, mark__in=['like', 'superlike']).\
        exclude(uid__in=friend_uid_list)

    liked_me_uid_list = [s.uid for s in swipe_list]

    return liked_me_uid_list
