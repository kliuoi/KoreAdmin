from server.core.msd.crub_base import CRUB_Base
from server.core.security.depends_auth import Auth
from server.db.db_casbin import get_casbin_enf
from server.core.response_base import errors


class CasbinCRUD(CRUB_Base):
    def __init__(self, auth: Auth):
        super().__init__(
            auth=auth,
        )
        self.enf = get_casbin_enf()

    async def _get_enf(self):
        if self.enf is None:
            from server.db.db_casbin import get_casbin_enf
            self.enf = await get_casbin_enf()
        return self.enf

    async def get_policy_list(self, role: int = None):
        """获取策略列表"""
        enf = await self._get_enf()
        if role is not None:
            data = await enf.get_filtered_named_policy("p", 0, str(role))
        else:
            data = await enf.get_policy()
        return data

