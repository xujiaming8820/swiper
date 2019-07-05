"""
业务模块配置
"""

# 云之讯短信平台配置
YZX_SMS_URL = 'https://open.ucpaas.com/ol/sms/sendsms'

YZX_SMS_PARAMS = {
    'sid': '30d6bcfa572af4d93c267f6b5aef5716',
    'token': 'abca1e88c1eb1a5e43a67cb9fdab9b61',
    'appid': '0446dca0e4134eb2ad2bad60f237d948',
    'templateid': '481924',
    'param': None,
    'mobile': None
}

# 缓存 key prefix
VERIFY_CODE_CACHE_PREFIX = 'verfiy_code:%s'

# 七牛云配置
QN_ACCESS_KEY = 'wsi-f-ZsS_Nbj4xfCHPGXB3K0_NqllAsXlkkkbdJ'
QN_SECRET_KEY = 'N3sr80gxxXF9Ed35t8CxFrOeFriSYE87iiz6lFug'
QN_BUCKET = 'swiper'
QN_HOST = 'http://pu420clqe.bkt.clouddn.com'