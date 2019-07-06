"""
业务返回码，错误码配置
"""

OK = 0

# 用户系统
# 1001 = '手机号格式错误'
PHONE_NUM_ERR = 1001  # 手机号格式错误
SMS_SEND_ERR = 1002  # 短信发送失败
VERIFY_CODE_ERR = 1003  # 验证码错误
LOGIN_REQUIRED = 1004  # 未登录
AVATAR_UPLOAD_ERR = 1005  # AVATAR 上传失败

# 社交系统
SWIPE_ERR = 2001  # 滑动动作错误
SID_ERR = 2002  # 被滑动者不存在


class LogicException(Exception):
    def __init__(self, code):
        self.code = code


class LogicError(Exception):
    code = None


def gen_logic_error(name, code):
    return type(name, (LogicError,), {'code': code})


# 用户系统
PhoneNumError = gen_logic_error('PhoneNumError', 1001)  # 手机号格式错误
SmsSendError = gen_logic_error('SmsSendError', 1002)  # 短信发送失败
VerifyCodeError = gen_logic_error('VerifyCodeError', 1003)  # 验证码错误
LoginRequiredError = gen_logic_error('LoginRequiredError', 1004)  # 未登录
AvatarUploadError = gen_logic_error('AvatarUploadError', 1005)  # 上传形象失败

# 社交系统
SwipeError = gen_logic_error('SwipeError', SWIPE_ERR)  # 滑动动作错误
SidError = gen_logic_error('SidError', SID_ERR)  # 被滑动者不存在
RewindLimitError = gen_logic_error('RewindLimitError', 2003)  # 返回次数超过每日上限