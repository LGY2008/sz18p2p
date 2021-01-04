from config import HOST


class ApiTender:
    # 初始化
    def __init__(self, session):
        # 获取session
        self.session = session
        # 投资url
        self.__url_tender = HOST + "/trust/trust/tender"
        # 投资列表url
        self.__url_tender_list = HOST + "/loan/tender/mytenderlist"

    # 投资
    def api_tender(self, tendder_id=642, depositCertificate=-1, amount=100):
        # 定义请求参数
        data = {
            "id": tendder_id,
            "depositCertificate": depositCertificate,
            "amount": amount
        }
        # 调用post方法
        return self.session.post(url=self.__url_tender, data=data)

    # 获取投资列表
    def api_tender_list(self):
        # 定义请求参数
        data = {
            "status": "tender"
        }
        # 调用post方法
        return self.session.post(url=self.__url_tender_list, data=data)

