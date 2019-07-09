from django.urls import path

from social import api

urlpatterns = [
    path('recommend', api.recommend),
    path('like', api.like),
    path('dislike', api.dislike),
    path('superlike', api.superlike),
    path('rewind', api.rewind),
    path('liked_me', api.liked_me),
    path('friends', api.friends),
    path('top10', api.top10),
]
