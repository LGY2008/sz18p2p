import pytest
import requests
from time import sleep

from api import log
from api.api_reg_login import ApiRegLogin
from util import read_json, common_assert, clear_data


class TestRegLogin:
    def setup_class(self):
        log.info("正在调用清除测试数据...")
        # 清除数据
        clear_data()
    # 初始化
    def setup(self):
        # 获取session
        self.session = requests.session()
        # 实例化ApiRegLogin对象
        self.api_reg = ApiRegLogin(self.session)

    # 结束
    def teardown(self):
        # 关闭Session
        self.session.close()

    # 1、注册图片验证码 接口测试方法
    @pytest.mark.parametrize(("random", "expect_code"), read_json("reg_login.json", "img_code"))
    def test01_img_code(self, random, expect_code):
        result = self.api_reg.api_get_img_code(random)
        try:
            common_assert(result, response_code=expect_code)
            log.info("断言通过，断言信息：{}".format(expect_code))
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    # 2、注册手机验证码 接口测试方法
    @pytest.mark.parametrize(("phone", "imgVerifyCode", "response_code", "expect_msg"),
                             read_json("reg_login.json", "sms_code"))
    def test02_sms_code(self, phone, imgVerifyCode, response_code, expect_msg):
        # 1、图片验证码
        self.api_reg.api_get_img_code(123234)
        # 2、调用短信验验证码
        result = self.api_reg.api_get_sms_code(phone, imgVerifyCode)
        print(result.json())
        try:
            common_assert(result, response_code=response_code)
            if expect_msg == "100":
                common_assert(result, status=expect_msg)
            else:
                common_assert(result, expect_msg=expect_msg)
                log.info("断言通过，断言信息：{}".format(expect_msg))
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    # 3、注册 接口测试方法
    @pytest.mark.parametrize(
        ("phone", "password", "verifycode", "phone_code", "dy_server", "invite_phone", "expect_msg"),
        read_json("reg_login.json", "reg_data"))
    def test03_register(self,
                        phone,
                        password,
                        verifycode,
                        phone_code,
                        dy_server,
                        invite_phone,
                        expect_msg):
        # 1、图片验证码
        self.api_reg.api_get_img_code(123343)
        # 2、短信验证验证码
        self.api_reg.api_get_sms_code(phone, verifycode)
        # 3、注册
        result = self.api_reg.api_post_register(phone=phone,
                                                password=password,
                                                verifycode=verifycode,
                                                phone_code=phone_code,
                                                invite_phone=invite_phone)
        print("注册执行结果：", result.json())
        try:
            common_assert(result, expect_msg=expect_msg)
            log.info("断言通过，断言信息：{}".format(expect_msg))
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    @pytest.mark.parametrize(("keywords", "pwd", "expect_msg"), read_json("reg_login.json", "login_data"))
    def test04_login(self, keywords, pwd, expect_msg):
        # 1. 判断当前执行是否为错误次数验证
        # if pwd == "error":
        #     i = 0
        #     result = None
        #     while i <3:
        #         # 调用3次错误密码 让其锁定
        #         result = self.api_reg.api_post_login(keywords=keywords,
        #                                              password=pwd)
        #         i+=1
        #     # 断言锁定状态
        #     common_assert(result, expect_msg=expect_msg)
        #     # 锁定60秒
        #     sleep(60)
        #     # 锁定结束，正常登录
        #     result = self.api_reg.api_post_login(keywords="13600001111",
        #                                          password="test123")
        #     common_assert(result, expect_msg="登录成功")
        # 2. 非错误次数验证，执行登录
        result = self.api_reg.api_post_login(keywords=keywords,
                                             password=pwd)
        try:
            common_assert(result, expect_msg=expect_msg)
            log.info("断言通过，断言信息：{}".format(expect_msg))
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    @pytest.mark.parametrize(("status", "expect_msg"), read_json("reg_login.json", "is_login"))
    def test05_is_login(self, status, expect_msg):
        if status == "登录":
            # 登录
            self.api_reg.api_post_login(keywords="13600001111",
                                        password="test123")
        # 调用查询登录方法
        result = self.api_reg.api_get_login_status()
        try:
            common_assert(result,expect_msg=expect_msg)
            log.info("断言通过，断言信息：{}".format(expect_msg))
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

