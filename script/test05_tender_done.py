import pytest
import requests

from api import log
from api.api_get import ApiGet
from util import html_parser, clear_data


class TestTenderDone:
    def setup(self):
        # 获取session
        self.session = requests.session()
        # 获取ApiLoginReg对象
        self.reg_login = ApiGet.get_apireglogin(self.session)

    def teardown(self):
        # 关闭Session对象
        self.session.close()

    def teardown_class(self):
        log.info("正在调用清除测试数据...")
        # 清除数据
        clear_data()
    @pytest.mark.mock
    def test01_tender_done(self):
        # 1、注册图片验证码接口
        self.reg_login.api_get_img_code(123123)
        # 2、注册手机验证码
        self.reg_login.api_get_sms_code("13600001111", "8888")
        # 3、注册
        r = self.reg_login.api_post_register("13600001111", "test123", "8888", "666666", None)
        print("-->>>>>注册：", r.json())
        # 4、登录
        r = self.reg_login.api_post_login("13600001111", "test123")
        print("-->>>>>登录：",r.json())
        # 5、请求开户
        result = ApiGet.get_apitrust(self.session).api_trust_register()
        # 6、三方开户
        r = html_parser(result)
        self.session.post(r[0], r[1])
        # 7、获取充值验证码
        ApiGet.get_apitrust(self.session).api_trust_verify_code()
        # 8、请求充值
        result = ApiGet.get_apitrust(self.session).api_trust_recharge(1000, 8888)
        r = html_parser(result)
        self.session.post(r[0], r[1])
        # 9、请求投资
        r = ApiGet.get_apitender(self.session).api_tender()
        # 10、三方投资
        r = html_parser(result)
        result = self.session.post(r[0], r[1])
        assert "OK" in result.text
