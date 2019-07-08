from libs.http import render_json
from vip.models import Vip


def vip_info(request):

    vip_info = []

    for vip in Vip.objects.all().exclude(level=0).order_by('level'):
        v_info = vip.to_dict()
        v_info['perms'] = []
        for perm in vip.perms:
            v_info['perms'].append(perm.to_dict())

        vip_info.append(v_info)


    result = {
        'vip_level': request.user.vip.level,
        'vip_info': vip_info,
    }

    return render_json(data=result)
