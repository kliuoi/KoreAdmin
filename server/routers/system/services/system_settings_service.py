from typing import Dict, Any
import os

from server.core.msd.service_base import Service_Base
from server.core.security.depends_auth import Auth
from server.core.config import settings, Settings

class SystemSettingsService(Service_Base):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)

    async def get_system_settings(self) -> Dict[str, Any]:
        """获取当前系统设置"""
        return {key: getattr(settings, key) for key in dir(settings) if not key.startswith('_')}

    async def update_system_settings(self, updated_settings: Dict[str, Any]) -> Dict[str, Any]:
        """更新系统设置"""
        for key, value in updated_settings.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
            else:
                raise ValueError(f"无效的设置项: {key}")
        return await self.get_system_settings()

    async def get_environment_variables(self) -> Dict[str, str]:
        """获取当前环境变量"""
        return dict(os.environ)

    async def update_environment_variables(self, updated_env_vars: Dict[str, str]) -> Dict[str, str]:
        """更新环境变量"""
        for key, value in updated_env_vars.items():
            os.environ[key] = value
        return await self.get_environment_variables()