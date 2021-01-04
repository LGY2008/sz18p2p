import json
import logging.handlers
from config import dir_path
import os
from bs4 import BeautifulSoup
import pymysql


# 1、读取json工具
def read_json(filename, data_type):
    # 1、组装文件路径
    file_path = dir_path + os.sep + "data" + os.sep + filename
    # 2、新增空列表，参数参数数据使用  [(),()]
    arr = []
    # 3、获取文件流
    with open(file_path, "r", encoding="utf-8") as f:
        # 遍历列表
        for data in json.load(f).get(data_type):
            # 获取每组字典数据并强转为元素 切掉 说明
            arr.append(tuple(data.values())[1:])
        # 返回数据
        return arr


# 2、公共断言方法
def common_assert(result, response_code=None, expect_msg=None, status=None):
    try:
        # 1. 断言response_code
        if response_code:
            assert int(response_code) == int(result.status_code), "断言失败，预期结果：{} 实际结果：{}".format(response_code,
                                                                                                result.status_code)
        # 2. 断言expect_msg
        if expect_msg:
            assert expect_msg in result.json().get("description"), "断言失败，预期结果：{} 实际结果：{}".format(expect_msg,
                                                                                                 result.json().get(
                                                                                                     "description"))
        # 3. 断言status
        if status:
            assert str(status) == str(result.json().get("status")), "断言失败，预期结果：{} 实际结果：{}".format(status,
                                                                                                  result.json().get(
                                                                                                      "status"))
    except Exception:
        raise


# 3、日志工具
class GetLog:
    # 定义日志器
    logger = None

    @classmethod
    def get_log(cls):
        if cls.logger is None:
            # 获取日志器
            cls.logger = logging.getLogger("lgy")
            # 设置日志级别
            cls.logger.setLevel(logging.INFO)
            # 存储文件
            filename = dir_path + os.sep + "log" + os.sep + "p2p.log"
            # 获取处理器（文件）
            th = logging.handlers.TimedRotatingFileHandler(filename=filename,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=3,
                                                           encoding="utf8")
            # 获取格式器
            fm = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            fmt = logging.Formatter(fm)
            # 将格式器添加到处理器中
            th.setFormatter(fmt)
            # 将处理器添加到日志器中
            cls.logger.addHandler(th)
        return cls.logger


# 4、解析html
def html_parser(result):
    # 1、提取html
    html = result.json().get("description").get("form")
    # 2、获取bs对象（解析html）
    bs = BeautifulSoup(html, "html.parser")
    # 3、提取url（action属性）
    url = bs.form.get("action")
    print("提取的url为：", url)
    arr = {}
    # 4、查找所有的input标签 并 遍历
    for input in bs.find_all("input"):
        # 5、提取name属性和value属性值 并存储到新的字典中
        arr[input.get("name")] = input.get("value")
    # 6、返回url和字典数据
    return url, arr


# 5、连接数据库
class DBUtil:
    # 1、执行sql语句方法
    @classmethod
    def exe_sql(cls, sql):
        # 1. 获取连接对象
        conn = pymysql.connect("52.83.144.39", "root", "Itcast_p2p_20191228", "czbk_member", 3306, charset="utf8")
        # 2. 获取游标对象
        cursor = conn.cursor()
        # 3、调用执行sql
        cursor.execute(sql)
        # 如果是查询 不用提交事务
        if sql.split()[0].lower() == "select":
            # 4、处理返回结果
            return cursor.fetchall()
        # 非查询 提交事务
        else:
            try:
                # 提交事务
                conn.commit()
                # 受影响的行数
                return cursor.rowcount
            except:
                conn.rollback()
        # 关闭连接
        cls.db_close(cursor, conn)

    # 2、关闭方法
    @classmethod
    def db_close(cls, cursor, conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 6、清除测试数据方法
def clear_data():
    # 1. 删除mb_member_info
    sql1 = """delete i.* from mb_member_info i inner join mb_member as m on m.id=i.member_id where m.phone in ("13600001111","13600001112","13600001113","13600001114","13600001115","13600001116");"""
    DBUtil.exe_sql(sql1)
    # 2、删除mb_member_login_log
    sql2 = """delete login.* from mb_member_login_log as login inner join mb_member m on m.id=login.member_id where m.phone in ("13600001111","13600001112","13600001113","13600001114","13600001115","13600001116");"""
    DBUtil.exe_sql(sql2)
    # 3、查询主表mb_member
    sql3 = """delete from mb_member where phone in ("13600001111","13600001112","13600001113","13600001114","13600001115","13600001116");"""
    DBUtil.exe_sql(sql3)
    # 4、查询注册日志 mb_member_register_log
    sql4 =  """delete from mb_member_register_log where phone in ("13600001111","13600001112","13600001113","13600001114","13600001115","13600001116");"""
    DBUtil.exe_sql(sql4)

if __name__ == '__main__':
    # print(read_json("reg_login.json", "sms_code"))
    # 参数化的格式 [(),()] [[],[]]
    GetLog.get_log().info("info 测试")
    GetLog.get_log().error("error 测试")
