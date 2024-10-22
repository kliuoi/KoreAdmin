from passlib.context import CryptContext

from server.core.config import settings


# 密码加密
def get_hash_password(password: str) -> str:
    """
    密码加密
    :param password: 明文密码
    :return: 密文密码
    """
    return CryptContext(schemes=[settings.PASSWORD_HASH_ALGORITHM]).hash(password)


# 密码校验
def verify_hash_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验
    :param plain_password: 明文密码
    :param hashed_password: 密文密码
    :return: 校验结果
    """
    return CryptContext(schemes=[settings.PASSWORD_HASH_ALGORITHM]).verify(plain_password, hashed_password)
