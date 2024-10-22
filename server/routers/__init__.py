from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from server.core.config import settings
from server.routers.system import system_router

# from server.routers.z_wjw_test import wjw_test_router as wjw_test_router
# from server.routers.z_scm import scm_router as scm_router


def register_router(app: FastAPI):

    app.include_router(system_router, prefix="/system")
    # app.include_router(wjw_test_router, prefix="/wjw")
    # app.include_router(scm_router, prefix="/scm")

    @app.get("/", summary="默认页面")
    def default_index():
        return RedirectResponse(url=settings.TOKEN_TEMP_REDIRECT)
