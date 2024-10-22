from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


def register_docs(app: FastAPI):
    """
    注册文档, CDN修改为本地, 不需要加载网络资源
    :param app:
    :return:
    """

    @app.get(app.docs_url, include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/docs/swagger-ui/@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="/static/docs/swagger-ui/@5.9.0/swagger-ui.css",
            swagger_favicon_url="/static/docs/favicon.ico",
        )

    @app.get(app.redoc_url, include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/docs/redoc_ui/redoc.standalone.js",
            redoc_favicon_url="/static/docs/favicon.ico",
        )
