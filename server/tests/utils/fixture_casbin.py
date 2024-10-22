from casbin import AsyncEnforcer

from server.core.config import settings
from server.db import async_adapter


async def get_test_casbin_enf() -> AsyncEnforcer:
    """
    获取casbin模型
    :return: None
    """
    model = AsyncEnforcer.new_model(path=settings.FASTAPI_CASBIN_CONF)
    enforcer = AsyncEnforcer(model, async_adapter)
    await enforcer.load_policy()
    return enforcer
