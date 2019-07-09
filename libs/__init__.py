from django.conf import settings
from redis import Redis

rds = Redis(**settings.REDIS)