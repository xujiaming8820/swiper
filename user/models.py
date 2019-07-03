from django.db import models


# Create your models here.
class User(models.Model):
    """
    phonenum    手机号码
    nickname    昵称
    sex         性别
    birth_year  年
    birth_month 月
    birth_day   日
    avatar      头像
    location    常驻地
    """
    phonenum = models.CharField(max_length=11, unique=True)
    nickname = models.CharField(max_length=32)
    sex = models.IntegerField(default=0)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(max_length=1)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=64)

    class Meta:
        db_table = 'users'
