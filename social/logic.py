import datetime

from common import errors
from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
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
    ret = Swiped.swipe(uid=uid, sid=sid, mark='supderlike')

    # 只有滑动成功，才可以进行好友匹配操作
    # 如果被滑动人喜欢过我，则建立好友关系
    if ret and Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)

    return ret
