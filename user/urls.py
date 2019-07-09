from django.urls import path

from user import api

urlpatterns = [
    path('verify-phone', api.verify_phone),
    path('login', api.login),
    path('get-profile', api.get_profile),
    path('set-profile', api.set_profile),
    path('upload-avatar', api.upload_avatar),
]
