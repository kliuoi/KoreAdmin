from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Any

from server.core.config import settings
from server.core.response_base.response_schema import CustomResponseCode


jinja_templates = Jinja2Templates(directory=settings.FASTAPI_TEMPLATE_FOLDER)


class ResponseModel(BaseModel):
    """
    统一返回模型

    E.g. ::
        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})

        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})

        @router.get('/test')
        def test() -> ResponseModel:
            res = CustomResponseCode.HTTP_200
            return ResponseModel(code=res.code, msg=res.msg, data={'test': 'test'})
    """

    # TODO: json_encoders 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
    # model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})
    model_config = ConfigDict(from_attributes=True)

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None


# 返回信息格式封装，包含正常返回和异常返回
class R:

    # @staticmethod
    # async def __response(*, res: CustomResponseCode | CustomResponse = None, data: Any | None = None) -> ResponseModel:
    #     """
    #     请求成功返回通用方法

    #     :param res: 返回信息
    #     :param data: 返回数据
    #     :return:
    #     """
    #     return ResponseModel(code=res.code, msg=res.msg, data=data)

    class ok(ORJSONResponse):
        """
        正常返回
        :param data: 返回数据
        :param code: 状态码
        :param msg: 返回信息
        :param headers: 响应头
        :return: dict
        """

        def __init__(
            self,
            status_code: int = CustomResponseCode.HTTP_200.code,
            headers: dict = None,
            code: int = CustomResponseCode.HTTP_200.code,
            msg: str = CustomResponseCode.HTTP_200.msg,
            data: dict = None,
            **kwargs: dict,
        ):
            content = {
                "code": code,
                "msg": msg,
                "data": data,
            }
            content.update(kwargs)
            super().__init__(status_code=status_code, headers=headers, content=content)

    class error(ORJSONResponse):
        """
        异常返回
        :param data: 返回数据
        :param code: 状态码
        :param msg: 返回信息
        :param headers: 响应头
        :return: dict
        """

        def __init__(
            self,
            status_code: int = CustomResponseCode.HTTP_200.code,
            headers: dict = None,
            code: int = CustomResponseCode.HTTP_400.code,
            msg: str = CustomResponseCode.HTTP_400.msg,
            data: dict = None,
            **kwargs: dict,
        ):
            content = {
                "code": code,
                "msg": msg,
                "data": data,
            }
            content.update(kwargs)
            super().__init__(status_code=status_code, headers=headers, content=content)

    # class render:
    #     """
    #     模板渲染函数
    #     :param name: 模板名称
    #     :param context: 上下文
    #     :return 返回渲染后的模板
    #     """

    #     def __init__(
    #         self,
    #         name: str,
    #         context: dict = None,
    #         headers: dict = None,
    #     ):
            
            # return jinja_templates.TemplateResponse(name=name, headers=headers, context=context)


    # @staticmethod
    # def ok(
    #     data: dict = None,
    #     code: int = CustomResponseCode.HTTP_200.code,
    #     msg: str = CustomResponseCode.HTTP_200.msg,
    #     headers: dict = None,
    #     **kwargs: dict,
    # ):
    #     """
    #     正常返回
    #     :param code: 状态码
    #     :param msg: 返回信息
    #     :param data: 返回数据
    #     :return: dict
    #     """
    #     content = {
    #         "status": code,
    #         "msg": msg,
    #         "data": data,
    #     }
    #     content.update(kwargs)
    #     return JSONResponse(status_code=code, content=content, headers=headers)

    # @staticmethod
    # def error(
    #     data: dict = [],
    #     code: int = CustomResponseCode.HTTP_500.code,
    #     msg: str = CustomResponseCode.HTTP_500.msg,
    #     headers: dict = None,
    #     **kwargs: dict,
    # ):
    #     """
    #     异常返回
    #     :param code: 状态码
    #     :param msg: 返回信息
    #     :param data: 返回数据
    #     :return: dict
    #     """
    #     content = {
    #         "status": code,
    #         "msg": msg,
    #         "data": data,
    #     }
    #     content.update(kwargs)
    #     return JSONResponse(status_code=code, content=content, headers=headers)

    @staticmethod
    def render(
        name: str,
        context: dict = None,
        headers: dict = None,
    ):
        """
        模板渲染函数
        :param name: 模板名称
        :param context: 上下文
        :return 返回渲染后的模板
        """
        return jinja_templates.TemplateResponse(name=name, context=context, headers=headers)


class errors:
    """
    全局异常类
    """

    # 鉴权失败需要重新登录
    class ReLoginException(HTTPException):
        """
        鉴权失败需要重新登录，重定向到登录页面
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 302, headers: dict = None, msg: str = "鉴权失败, 请重新登录"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    # Token错误
    class TokenException(HTTPException):
        """
        Token异常, 此异常适用于Token错误, 需要重新删除Token
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 401, headers: dict = None, msg: str = "Token错误"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    # 鉴权失败
    class AuthenticationException(HTTPException):
        """
        鉴权失败
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 401, headers: dict = None, msg: str = "鉴权失败, 请联系管理员"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    class PermissionException(HTTPException):
        """
        权限异常
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 401, headers: dict = None, msg: str = "权限不足"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    # 请求相关异常
    class RequestException(HTTPException):
        """
        请求返回相关异常
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 400, headers: dict = None, msg: str = "请求参数错误"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    # 请求资源不存在
    class NotFoundException(HTTPException):
        """
        请求资源不存在
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 404, headers: dict = None, msg: str = "请求的资源不存在"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    # 服务器异常
    class ServerException(HTTPException):
        """
        服务器异常
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 500, headers: dict = None, msg: str = "服务器异常"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)

    # 值错误
    class ValueError(HTTPException):
        """
        值错误
        :param status_code: 状态码
        :param headers: 响应头
        :param msg: 异常信息
        """

        def __init__(self, status_code: int = 400, headers: dict = None, msg: str = "值错误"):
            super().__init__(status_code=status_code, headers=headers, detail=msg)
