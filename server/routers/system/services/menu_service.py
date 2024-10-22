from typing import Any

from server.core.security.depends_auth import Auth
from server.core.response_base import errors
from server.core.msd.service_base import Service_Base
from server.core.security.passwd_encrypt import get_hash_password, verify_hash_password

from .. import schemas
from .. import crud
from .. import models


class MenuService(Service_Base):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)

    async def menu_get_info(
        self,
        *,
        obj: schemas.MenuQueryIn,
        v_schema: Any = None,
    ):
        """
        菜单详情查询
        """

        # 查询菜单详情
        return await crud.MenuCRUD(self.auth)._get(id=obj.id, name=obj.name, v_schema=v_schema)

    async def menu_update(
        self,
        *,
        obj: schemas.MenuUpdateIn,
        v_schema: Any = None,
    ):
        """
        菜单更新
        """
        db_menu = await crud.MenuCRUD(self.auth)._get(id=obj.id)
        if db_menu is None:
            raise errors.RequestException(msg="菜单不存在")

        try:
            db_menu = await crud.MenuCRUD(self.auth)._update(id=obj.id, obj_in=obj)
        except Exception:
            raise errors.RequestException(msg="菜单更新失败")

        return await self.out_dict(obj=db_menu, v_schema=v_schema)

    async def menu_delete(
        self,
        *,
        obj: schemas.MenuDeleteIn,
    ):
        """
        菜单删除
        """
        db_menu = await crud.MenuCRUD(self.auth)._get(id=obj.id, name=obj.name)
        if db_menu is None:
            raise errors.RequestException(msg="菜单不存在")

        try:
            await crud.MenuCRUD(self.auth)._delete(obj=db_menu)
        except Exception:
            raise errors.RequestException(msg="菜单删除失败")

        return True

    async def menu_create(
        self,
        *,
        obj: schemas.MenuCreateIn,
        v_schema: Any = None,
    ):
        """
        菜单创建
        """

        # 查询条件
        db_menu = await crud.MenuCRUD(self.auth)._get(name=obj.name)
        if db_menu:
            raise errors.RequestException(msg="菜单已存在")

        # 验证父菜单ID
        parent_menu = None
        if obj.parent_id:
            parent_menu = await crud.MenuCRUD(self.auth)._get(id=obj.parent_id)
            if not parent_menu:
                raise errors.RequestException(msg="父菜单不存在")

        try:
            # 创建新菜单
            new_menu = models.Sys_Menu(**obj.__dict__)

            # 如果有父菜单,将新菜单添加到父菜单的子菜单列表中
            if parent_menu:
                if parent_menu.children is None:
                    parent_menu.children = []
                parent_menu.children.append(new_menu)

            # 保存新菜单到数据库
            db_menu = await crud.MenuCRUD(self.auth)._create(obj=new_menu)

            # 如果有父菜单,更新父菜单
            if parent_menu:
                await crud.MenuCRUD(self.auth)._update(id=parent_menu.id, obj_in=parent_menu)

        except Exception as e:
            raise errors.RequestException(msg=f"菜单创建失败: {str(e)}")

        return await self.out_dict(obj=db_menu, v_schema=v_schema)
