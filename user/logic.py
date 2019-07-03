from common import utils
from lib import sms


def send_verify_code(phone_num):
    """
    发送验证码
    :param phone_num:
    :return:
    """
    # 生成验证码
    # 调用短信接口，发送验证码
    code = utils.gen_random_code(6)
    return sms.send(phone_num, code)
