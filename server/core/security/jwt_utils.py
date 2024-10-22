from datetime import timedelta
import jwt

from server.core.config import settings
from server.core.utils.timezone import timezone


async def token_create_access(data: str, expires_delta: timedelta = None) -> str:
    """
    生成JWT

    :param data: 通常是一个包含用户信息的字典
    :param expires_delta: 指定过期时间的时间差
    :return: JWT token
    """
    # 复制传入的data字典
    to_encode = {"sub": data}
    # 确定令牌的过期时间。如果提供了expires_delta参数，我们使用它；否则，我们使用默认的过期时间
    if expires_delta:
        expire = timezone.now() + expires_delta
    else:
        expire = timezone.now() + timedelta(minutes=settings.TOKEN_ACCESS_EXPIRE_MINUTES)
    # to_encode字典添加一个exp字段，这是JWT的标准字段，用于表示令牌的过期时间
    to_encode.update({"exp": expire})
    # 使用jose库的jwt.encode方法对字典进行编码，生成JWT。然后，返回生成的JWT
    jwt_encoded = jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    # 测试时间戳，可删除
    data = timezone.now()
    # 输出Token过期时间，以年月日时分秒的形式输出
    print("Token过期时间: {}".format(expire))

    # 输出当前时间，以年月日时分秒的形式输出
    print("Token当前时间: {}".format(data))

    # 输出Token剩余时间，以00:00:00的形式输出
    print("Token剩余时间(小时): {}".format(expire - data))

    return jwt_encoded


async def token_decode_access(token: str) -> dict:
    """
    验证并解码JWT
    接受一个JWT并尝试对其进行解码和验证。如果解码成功(即令牌有效且未过期),返回解码后的载荷(payload)
    如果发生任何错误(例如令牌无效、过期或签名不正确),捕获异常并返回None

    :param token: JWT token
    :return: JWT payload
    """
    try:
        payload = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        # 返回异常
        return None
