import random
import re

PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')


def is_phone_num(phone_num):
    """
    手机号码验证
    :param phone_num:
    :return:
    """

    return True if PHONE_PATTERN.match(phone_num) else False


def gen_random_code(length=4):
    """
    生成指定长度的随机码
    :param length:
    :return:
    """
    if length <= 0:
        length = 1

    code = random.randrange(10 ** (length - 1), 10 ** length)

    return str(code)
