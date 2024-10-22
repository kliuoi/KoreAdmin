from asgiref.sync import sync_to_async
import re

from server.core.response_base import errors


# 校验手机号格式
@sync_to_async
def check_phone(self, phone: str) -> bool:
    """
    校验手机号格式

    :param phone: 手机号
    :return:
    """
    if len(phone) != 11 or not phone.isdigit():
        raise errors.ValueError(msg="请输入正确的手机号码")
    pattern = re.compile(r"^1[3-9]\d{9}$")
    result = pattern.match(phone) is not None
    if not result:
        raise errors.ValueError(msg="请输入正确的手机号码")

    return True


# 校验邮箱格式
@sync_to_async
def check_email(self, email: str) -> bool:
    """
    校验邮箱格式
    :param email: 邮箱
    :return:
    """
    # TODO 邮箱格式校验
    pattern = re.compile(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]{2,6}$")
    result = pattern.match(email) is not None
    if not result:
        raise ValueError("请输入正确的邮箱地址")
    return True
