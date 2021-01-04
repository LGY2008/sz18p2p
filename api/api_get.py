from api.api_approve import ApiApprove
from api.api_reg_login import ApiRegLogin
from api.api_tender import ApiTender
from api.api_trust import ApiTrust


class ApiGet:
    """统一管理api对象，避免使用中多次导包"""

    # 返回ApiApprove对象
    @classmethod
    def get_apiapprove(cls, session):
        return ApiApprove(session)

    # 返回ApiRegLogin对象
    @classmethod
    def get_apireglogin(cls, session):
        return ApiRegLogin(session)

    # 返回ApiTrust对象
    @classmethod
    def get_apitrust(cls,session):
        return ApiTrust(session)

    # 返回ApiTender对象
    @classmethod
    def get_apitender(cls, session):
        return ApiTender(session)