import pytest
import requests

from api import log
from api.api_get import ApiGet
from util import common_assert, read_json


class TestApprove:
    # 初始化
    def setup(self):
        # 获取session
        self.session = requests.session()
        # 获取ApiApprove对象
        self.approve = ApiGet.get_apiapprove(self.session)

    # 结束
    def teardown(self):
        # 关闭session
        self.session.close()

    # 开户认证接口测试方法
    @pytest.mark.parametrize(("realname", "card_id", "expect_status"), read_json("approve.json", "approve"))
    def test01_approve(self, realname, card_id, expect_status):
        # 1、获取ApiRegLogin对象并调用登录
        ApiGet.get_apireglogin(self.session).api_post_login("13600001111", "test123")
        # 2、认证
        result = self.approve.api_approve(realname=realname, card_id=card_id)
        try:
            # 断言
            common_assert(result, status=expect_status)
            # 日志结果
            log.info("断言成功，断言信息：".format(expect_status))
        except Exception as e:
            # 错误日志
            log.error(e)
            # 抛异常
            raise

    # 认证查询接口测试方法
    @pytest.mark.parametrize(("status","expect_msg"),read_json("approve.json","get_approve"))
    def test02_get_approve(self, status, expect_msg):
        if status == "已登录":
            # 调用登录
            ApiGet.get_apireglogin(self.session).api_post_login("13600001111", "test123")
            # 调用查询方法
            result = self.approve.api_get_approve()
            print("查询结果为 ：", result.json())
            try:
                # 断言
                assert expect_msg in result.json().get("phone")
                # 记录日志
                log.info("认证查询接口断言成功！，断言内容：{}".format(expect_msg))
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise
        elif status == "未登录":
            # 调用查询方法
            result = self.approve.api_get_approve()
            try:
                # 断言
                assert "立即登录" in result.text
                # 记录日志
                log.info("认证查询接口断言成功！，断言内容：{}".format(expect_msg))
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise
