from django.urls import path

from user import api

urlpatterns = [
    path('verify-phone', api.verify_phone),
    path('user_login',api.user_login),
]
