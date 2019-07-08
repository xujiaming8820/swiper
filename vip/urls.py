from django.urls import path

from vip import api

urlpatterns = [
    path('vip_info', api.vip_info)
]