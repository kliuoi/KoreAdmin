from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pydantic.errors import PydanticUserError

from server.core.config import settings
from server.core.response_base import errors
from server.core.response_base.response_schema import (
    StandardResponseCode,
    CUSTOM_USAGE_ERROR_MESSAGES,
    CUSTOM_VALIDATION_ERROR_MESSAGES,
)


async def _validation_exception_handler(request: Request, e: RequestValidationError | ValidationError):
    """
    数据验证异常处理

    :param e:
    :return:
    """
    errors = []
    for error in e.errors():
        custom_message = CUSTOM_VALIDATION_ERROR_MESSAGES.get(error["type"])
        if custom_message:
            ctx = error.get("ctx")
            if not ctx:
                error["msg"] = custom_message
            else:
                error["msg"] = custom_message.format(**ctx)
                ctx_error = ctx.get("error")
                if ctx_error:
                    error["ctx"]["error"] = (
                        ctx_error.__str__().replace("'", '"') if isinstance(ctx_error, Exception) else None
                    )
        errors.append(error)
    error = errors[0]
    if error.get("type") == "json_invalid":
        message = "json解析失败"
    else:
        error_input = error.get("input")
        field = str(error.get("loc")[-1])
        error_msg = error.get("msg")
        message = f"{error_msg}{field}，输入：{error_input}"
    msg = f"请求参数非法: {message}"
    data = {"errors": errors}
    content = {
        "code": StandardResponseCode.HTTP_422,
        "msg": msg,
        "data": data,
    }
    return JSONResponse(status_code=422, content=content)


# 注册全局异常处理
def register_exception(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def fastapi_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        fastapi 数据验证异常处理

        :param request:
        :param exc:
        :return:
        """
        return await _validation_exception_handler(request, exc)

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """
        pydantic 数据验证异常处理

        :param request:
        :param exc:
        :return:
        """
        return await _validation_exception_handler(request, exc)

    @app.exception_handler(PydanticUserError)
    async def pydantic_user_error_handler(request: Request, exc: PydanticUserError):
        """
        Pydantic 用户异常处理

        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=StandardResponseCode.HTTP_422,
            content={
                "code": StandardResponseCode.HTTP_422,
                "msg": CUSTOM_USAGE_ERROR_MESSAGES.get(exc.code),
                "data": None,
            },
        )

    @app.exception_handler(errors.ReLoginException)
    async def authentication_exception_handler(request: Request, exc: errors.ReLoginException):
        """
        异常处理登录页面重定向
        自定义异常处理, 把错误改为重定向到登录页面

        :param request:
        :param exc:
        :return:
        """
        return RedirectResponse(url=settings.TOKEN_TEMP_REDIRECT, status_code=exc.status_code, headers=exc.headers)

    @app.exception_handler(HTTPException)
    async def request_exception_handler(request: Request, exc: HTTPException):
        """
        RequestException 异常处理
        自定义异常处理, 把异常信息改为json格式返回

        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            headers=exc.headers,
            status_code=exc.status_code,
            content={"status": exc.status_code, "msg": exc.detail},
        )
