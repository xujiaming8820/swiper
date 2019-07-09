from django.shortcuts import render

# Create your views here.
from common import errors
from libs.http import render_json
from social import logic
from social.models import Swiped, Friend
from social.permissions import has_perm
from user.models import User


def recommend(request):
    """
    根据当前用户的 profile 筛选符合条件的用户
    :param request:
    :return:
    """
    recm_users = logic.recommend_users(request.user)

    users = [u.to_dict() for u in recm_users]

    return render_json(data=users)


def like(request):
    """
    喜欢
    :param request:
    :return:
    """
    sid = int(request.POST.get('sid'))
    user = request.user

    matched = logic.like_someone(user.id, sid)

    return render_json(data={'matched': matched})


@has_perm('superlike')
def superlike(request):
    """
    超级喜欢
    :param request:
    :return:
    """
    sid = int(request.POST.get('sid'))
    user = request.user

    matched = logic.superlike_someone(user.id, sid)

    return render_json(data={'matched': matched})


def dislike(request):
    """
    不喜欢
    :param request:
    :return:
    """
    sid = int(request.POST.get('sid'))
    user = request.user

    Swiped.swipe(uid=user.id, sid=sid, mark='dislike')

    return render_json()


@has_perm('rewind')
def rewind(request):
    """
    反悔
    不需要从客户端获取数据
    :param request:
    :return:
    """
    user = request.user
    logic.rewind(user)

    return render_json()


@has_perm('liked_me')
def liked_me(request):
    """
    喜欢我的人列表
    :param request:
    :return:
    """
    liked_me_uid_list = logic.liked_me(request.user)

    users = User.objects.filter(id__in=liked_me_uid_list)

    user_list = [u.to_dict() for u in users]

    return render_json(data=user_list)


def friends(request):
    """
    好友列表
    :param request:
    :return:
    """
    friend_id_list = Friend.friend_list(request.user.id)

    my_friends = User.objects.filter(id__in=friend_id_list)
    friend_list = [u.to_dict() for u in my_friends]

    return render_json(data=friend_list)


def top10(request):
    """
    获取人气排行榜
    :param request:
    :return:
    """
    ret_data = logic.get_top_rank(10)

    rank_data = []

    for user, score in ret_data:
        user_dict = user.to_dict()
        user_dict['score'] = score
        rank_data.append(user_dict)

    return render_json(data=rank_data)
