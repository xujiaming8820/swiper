from django.shortcuts import render


# Create your views here.
from common import errors
from libs.http import render_json
from social import logic


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
    sid = request.POST.get('sid')
    user = request.user

    if logic.like_someone(user.id, sid):
        return render_json()
    else:
        return render_json(errors.LIKE_ERR)


def dislike(request):
    return None


def superlike(request):
    return None


def rewind(request):
    return None


def liked_me(request):
    return None