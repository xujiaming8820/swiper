from django.utils.deprecation import MiddlewareMixin

from common import errors
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    WHITE_LIST = [
        '/api/user/verify-phone',
        '/api/user/user-login',
    ]

    def process_request(self, request):
        if request.path in self.WHITE_LIST:
            return

        uid = request.session.get('uid')

        if uid is None:
            return render_json(code=errors.LOGIN_REQUIRED)

        request.user = User.objects.get(id=uid)
