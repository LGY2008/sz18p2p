from config import HOST
from api import log


class ApiRegLogin:
    # 初始化
    def __init__(self, session):
        # 初始化session
        self.session = session
        # 注册图片验证码url
        self.__url_img = HOST + "/common/public/verifycode1/{}"
        # 注册手机验证码url
        self.__url_sms = HOST + "/member/public/sendSms"
        # 注册url
        self.__url_reg = HOST + "/member/public/reg"
        # 登录url
        self.__url_login = HOST + "/member/public/login"
        # 查询登录url
        self.__url_is_login = HOST + "/member/public/islogin"

    # 1、获取图片验证码接口封装
    def api_get_img_code(self, num):
        log.info("正在调用获取图片验证码接口，请求url:{}".format(self.__url_img.format(num)))
        return self.session.get(self.__url_img.format(num))

    # 2、获取短信验证码接口封装
    def api_get_sms_code(self, phone, imgVerifyCode):
        # 1、定义参数
        data = {
            "phone": phone,
            "imgVerifyCode": imgVerifyCode,
            "type": "reg"
        }
        log.info("正在调用获取短信验证码接口，请求url:{}, 请求数据：{}".format(self.__url_sms, data))
        # 2、请求
        return self.session.post(self.__url_sms, data=data)

    # 3、注册接口封装
    def api_post_register(self, phone, password, verifycode, phone_code, invite_phone=None):
        # 1、定义请求参数
        data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code": phone_code,
            "dy_server": "on",
            "invite_phone": invite_phone
        }
        log.info("正在注册接口，请求url:{}, 请求数据：{}".format(self.__url_reg, data))
        # 2、调用post
        return self.session.post(url=self.__url_reg, data=data)

    # 4、登录接口封装
    def api_post_login(self, keywords, password):
        # 1、定义请求参数
        data = {
            "keywords": keywords,
            "password": password
        }
        log.info("正在登录接口，请求url:{}, 请求数据：{}".format(self.__url_login, data))
        # 2、调用post
        return self.session.post(url=self.__url_login, data=data)

    # 5、查询登录状态接口封装
    def api_get_login_status(self):
        log.info("正在查询登录状态接口，请求url:{}".format(self.__url_login))
        return self.session.post(url=self.__url_is_login)
