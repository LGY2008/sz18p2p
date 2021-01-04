import pytest
import requests

from api import log
from api.api_get import ApiGet
from util import html_parser, common_assert, read_json


class TestTender:
    # 初始化
    def setup(self):
        # 获取session
        self.session = requests.session()
        # 获取ApiTender实例
        self.tender = ApiGet.get_apitender(self.session)
        # 登录
        ApiGet.get_apireglogin(self.session).api_post_login("13600001111", "test123")

    # 结束
    def teardown(self):
        self.session.close()

    # 1、投资接口测试
    @pytest.mark.parametrize(("tendder_id","depositCertificate","amount","expect_msg"),read_json("tender.json","tender"))
    def test01_tender(self, tendder_id, depositCertificate, amount, expect_msg):
        # 调用投资接口
        result = self.tender.api_tender(tendder_id, depositCertificate, amount)
        try:
            # 断言
            common_assert(result, expect_msg=expect_msg)
            log.info("断言成功！预期结果：{} 实际结果：{}".format(expect_msg, result.json().get("description")))
        except Exception as e:
            log.error(e)
            raise

    # 2、三方投资接口测试
    @pytest.mark.parametrize(("expect_msg",),read_json("tender.json","tender_public"))
    def test02_tender_public(self, expect_msg):
        # 1、调用投资
        result = self.tender.api_tender()
        # 2、提取html
        r = html_parser(result)
        # 3、请求三方接口
        result = self.session.post(r[0], r[1])
        try:
            # 4、断言
            assert expect_msg in result.text
            log.info("断言成功！预期结果：{} 实际结果：{}".format(expect_msg, result.text))
        except Exception as e:
            log.error(e)
            raise

    # 3、获取投资列表 接口测试
    @pytest.mark.parametrize(("expect_msg",),read_json("tender.json","tender_list"))
    def test03_tender_list(self, expect_msg):
        # 调用投资列表
        result = self.tender.api_tender_list()
        print("结果为----->：", result.json())
        try:
            # 断言
            assert int(expect_msg) == int(result.json().get("items")[0].get("loanId"))
            log.info("断言成功！预期结果：{} 实际结果：{}".format(expect_msg, result.json().get("items")[0].get("loanId")))
        except Exception as e:
            log.error(e)
            raise
