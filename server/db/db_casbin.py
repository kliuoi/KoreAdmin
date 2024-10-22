from casbin_async_sqlalchemy_adapter import Adapter
from casbin import AsyncEnforcer

from server.core.config import settings

from .db_datebase import async_engine
from .models import Sys_Casbin_Rule


async_adapter = Adapter(async_engine, db_class=Sys_Casbin_Rule)


async def get_casbin_enf() -> AsyncEnforcer:
    """
    获取casbin模型

    :return:
    """
    model = AsyncEnforcer.new_model(path=settings.FASTAPI_CASBIN_CONF)
    enforcer = AsyncEnforcer(model, async_adapter)
    await enforcer.load_policy()
    return enforcer
