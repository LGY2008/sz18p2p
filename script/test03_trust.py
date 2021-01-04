import pytest
import requests

from api import log
from api.api_get import ApiGet
from util import common_assert, html_parser, read_json


class TestTrust:
    # 初始化
    def setup(self):
        # 1、获取session
        self.session = requests.session()
        # 2、获取ApiGet
        self.trust = ApiGet.get_apitrust(self.session)
        # 3、调用登录
        ApiGet.get_apireglogin(self.session).api_post_login("13600001111", "test123")

    # 结束
    def teardown(self):
        self.session.close()

    # 1、开户接口 测试方法
    @pytest.mark.parametrize(("expect_msg",), read_json("trust.json", "trust_reg"))
    def test01_trust_register(self, expect_msg):
        # 1、调用开户
        result = self.trust.api_trust_register()
        # 2、开户结果断言 form
        print("开户结果为：", result.json())
        r = html_parser(result)
        # 3、请求三方开户
        result = self.session.post(url=r[0], data=r[1])
        try:
            # 4、三方开户结果断言
            assert expect_msg in result.text
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    # 2、充值验证码接口测试方法
    @pytest.mark.parametrize(("response_code",), read_json("trust.json", "trust_verify_code"))
    def test02_trust_verify_code(self, response_code):
        # 调用 充值验证码接口
        result = self.trust.api_trust_verify_code()
        try:
            # 断言
            common_assert(result, response_code=response_code)
            log.info("断言充值验证码成功，断言信息：{}".format(response_code))
        except Exception as e:
            log.error(e)
            raise

    # 3、充值接口测试方法
    @pytest.mark.parametrize(("amount", "img_code", "expect_msg"), read_json("trust.json", "trust_recharge"))
    def test03_trust_recharge(self, amount, img_code, expect_msg):
        # 调用 充值验证码
        self.trust.api_trust_verify_code()
        # 调用 充值接口
        result = self.trust.api_trust_recharge(amount, img_code)
        if expect_msg == "OK":
            # html提取
            r = html_parser(result)
            # 3、三方充值
            result = self.session.post(url=r[0], data=r[1])
            try:
                # 断言
                assert expect_msg in result.text
                log.info("断言充值成功，断言信息：{} 实际结果为：{}".format(expect_msg, result.text))
            except Exception as e:
                log.error(e)
                raise
        else:
            try:
                # 断言
                common_assert(result, expect_msg=expect_msg)
                log.info("断言充值成功，断言信息：{} 实际结果为：{}".format(expect_msg, result.text))
            except Exception as e:
                log.error(e)
                raise
