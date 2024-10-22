from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any

from server.core.config import settings
from server.core.security.depends_auth import Auth
from server.core.msd.crub_base import CRUB_Base

from .. import models
from .. import schemas


class RoleCRUD(CRUB_Base):
    """
    角色增删改查
    """

    def __init__(self, auth: Auth):
        super().__init__(
            auth=auth,
            model=models.Sys_Role,
        )
