from server.core.security.depends_auth import Auth

from .tools_base import Tools_Base

class Service_Base(Tools_Base):
    def __init__(self, auth: Auth) -> None:
        self.auth = auth
        self.db = auth.db
        self.user = auth.user
