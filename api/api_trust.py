from config import HOST


class ApiTrust:
    # 初始化
    def __init__(self, session):
        self.session = session
        # 开户url
        self.__url_trust = HOST + "/trust/trust/register"
        # 充值验证码url
        self.__url_vericy_code = HOST + "/common/public/verifycode/0.112312"
        # 充值url
        self.__url_trust_recharge = HOST + "/trust/trust/recharge"

    # 1、请求开户 接口封装
    def api_trust_register(self):
        # 调用post方法
        return self.session.post(self.__url_trust)

    # 2、请求充值验证码 接口封装
    def api_trust_verify_code(self):
        # 调用post方法
        return self.session.post(self.__url_vericy_code)

    # 3、请求充值 接口封装
    def api_trust_recharge(self, amount, img_code):
        # 定义请求参数
        data = {
            "paymentType": "chinapnrTrust",
            "amount": amount,
            "formStr": "reForm",
            "valicode": img_code
        }
        # 调用post方法
        return self.session.post(self.__url_trust_recharge, data=data)
