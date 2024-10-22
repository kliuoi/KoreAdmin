from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any

from server.core.msd.crub_base import CRUB_Base
from server.core.security.depends_auth import Auth
from server.core.response_base import errors

from .. import models
from .. import schemas


class MenuCRUD(CRUB_Base):
    """
    菜单增删改查
    """

    def __init__(self, auth: Auth):
        super().__init__(
            auth=auth,
            model=models.Sys_Menu,
        )

    async def menus_get_tree_list(
        self,
        *,
        v_schema: Any = None,
    ):
        """
        菜单列表树形结构
        """

        # 展示所有菜单，有上下级关系，返回树形结构
        async def build_menu_tree(menu: models.Sys_Menu):
            menu_dict = await self.select_as_dict(menu)

            # 查询子菜单
            result = await self.db.execute(select(models.Sys_Menu).where(models.Sys_Menu.parent_id == menu.id))
            children = result.scalars().all()
            # 判断是否有子菜单
            if children:
                menu_dict["children"] = []
                for child in children:
                    menu_dict["children"].append(await build_menu_tree(child))
            return menu_dict

        result = await self.db.execute(select(models.Sys_Menu).where(models.Sys_Menu.parent_id is None))
        top_level_menus = result.scalars().all()

        menu_tree = []
        for menu in top_level_menus:
            menu_tree.append(await build_menu_tree(menu))
        return menu_tree
