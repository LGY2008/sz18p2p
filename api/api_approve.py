from config import HOST


class ApiApprove:
    # 初始化
    def __init__(self, session):
        # 初始化session
        self.session = session
        # 开户认证url
        self.__url_approve = HOST + "/member/realname/approverealname"
        # 获取认证url
        self.__url_get_approve = HOST + "/member/member/getapprove"

    # 1、开户接口封装封装
    def api_approve(self, realname, card_id):
        # 1. 定义请求参数
        data = {
            "realname": realname,
            "card_id": card_id
        }
        # 2. 调用post方法
        # 重点：请求信息头类型为多消息体multipart/form-data
        # 解决：传递多个参数类型（大于1个），自动切换为：multipart
        return self.session.post(url=self.__url_approve, data=data, files={"x": "y"})

    # 2、获取认证信息接口封装
    def api_get_approve(self):
        return self.session.post(self.__url_get_approve)