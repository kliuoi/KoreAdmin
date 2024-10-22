from fastapi import APIRouter, Depends
import requests

from server.core.security.depends_auth import Auth, auth_support

api = APIRouter()


@api.get("/get_class", summary="通过班级链接获取班级信息")
async def get_class(
    class_link: str,
    auth: Auth = Depends(auth_support.get_db),
):
    back = requests.get(class_link)
    # 获取班级信息

    return back.text
