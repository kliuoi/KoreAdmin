from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal, Dict, Any
import os


class Settings(BaseSettings):

    # ================================================== 应用配置 ==================================================

    # 应用运行地址
    FASTAPI_HOST: str = "127.0.0.1"
    # 应用运行端口
    FASTAPI_PORT: int = 8888

    # 应用名称
    FASTAPI_NAME: str = "KoreAdmin"
    # 应用版本
    FASTAPI_VERSION: str = "v0.1.0"
    # 应用描述
    FASTAPI_DESCRIPTION: str = "KoreAdmin是一个基于FastAPI的后台管理系统"
    # 应用docs文档地址
    FASTAPI_DOCS_URL: str = "/docs"
    # 应用redoc文档地址
    FASTAPI_REDOC_URL: str = "/redoc"

    # 是否允许用户接口注册：是:允许注册-True,否:不允许注册-False
    FASTAPI_ALLOW_REGISTER: bool = True
    # 是否开启调试模式：是-True,否-False
    FASTAPI_DEBUG: bool = True
    # 应用环境变量, 开发环境-dev, 生产环境-pro
    # FASTAPI_ENV: Literal["dev", "pro"] = "dev"
    # 时区设置
    DATETIME_TIMEZONE: str = "Asia/Shanghai"

    def get_fastapi_params(self) -> Dict[str, Any]:
        return {
            "title": self.FASTAPI_NAME,
            "version": self.FASTAPI_VERSION,
            "description": self.FASTAPI_DESCRIPTION,
            "docs_url": self.FASTAPI_DOCS_URL,
            "redoc_url": self.FASTAPI_REDOC_URL,
            "debug": self.FASTAPI_DEBUG,
        }

    # ================================================== JWT认证配置 ==================================================

    # 密码加密算法：bcrypt、pbkdf2_sha256、pbkdf2_sha512、sha256_crypt、sha512_crypt
    PASSWORD_HASH_ALGORITHM: Literal["sha512_crypt"] = "sha512_crypt"
    # JWT密钥, 应在生产环境中更换为更安全的值
    JWT_SECRET_KEY: str = "a_very_secret_key"
    # JWT使用的签名算法HS256（HMAC使用SHA-256散列函数）
    JWT_ALGORITHM: Literal["HS256"] = "HS256"
    # 默认的过期时间（30分钟）
    TOKEN_ACCESS_EXPIRE_MINUTES: int = 1
    # 刷新Token的过期时间, 以秒为单位, 需要小于Token的过期时间
    # TOKEN_REFRESH_EXPIRE_MINUTES: int = 60 * 10

    # ================================================== 鉴权配置 ==================================================

    # 认证Token的模板重定向页面URL
    TOKEN_TEMP_REDIRECT: str = "/system/v1/auth/login"
    # 认证Token的接口URL
    TOKEN_URL: str = "/system/v1/api/auth/token"
    # Swagger UI登录接口URL
    SWAGGER_LOGIN_URL: str = "/system/v1/api/auth/swagger_login"
    # 鉴权模式：casbin、role_menu
    PERMISSION_MODE: Literal["casbin", "role_menu"] = "casbin"
    # 认证URL白名单
    TOKEN_EXCLUDE: list[str] = [
        TOKEN_TEMP_REDIRECT,
        TOKEN_URL,
        SWAGGER_LOGIN_URL,
    ]
    # 认证存储模式：cookie、header
    AUTHORIZATION_MODE: Literal["cookie", "header"] = "cookie"
    # 默认的token鉴权名称
    AUTHORIZATION_NAME: str = "Authorization"

    # ================================================== 应用目录配置 ==================================================

    # 获取基本目录/server
    FASTAPI_BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # server/static
    FASTAPI_STATIC_FOLDER: str = "server/static"
    # 应用模板路径
    FASTAPI_TEMPLATE_FOLDER: str = "server/templates"

    # Casbin配置文件路径
    FASTAPI_CASBIN_CONF: str = os.path.join(FASTAPI_BASE_DIR, "core", "config", "cas_rbac_model.conf")

    # 应用文件存储路径
    # FASTAPI_UPLOAD_DIR = os.getenv('FASTAPI_UPLOAD_DIR', os.path.join(FASTAPI_ROOT_PATH, '/uploads'))
    # 正式图片路径
    # FASTAPI_IMAGE_PATH = FASTAPI_UPLOAD_DIR + '/images'
    # 临时文件路径
    # FASTAPI_TEMP_PATH = FASTAPI_UPLOAD_DIR + '/temp'
    # 应用图片域名
    # FASTAPI_IMAGE_URL = os.getenv('FASTAPI_IMAGE_URL', '')

    # ================================================== 数据库配置 ==================================================

    # 使用数据库驱动：sqlite、mysql、postgresql、oracle、mssql
    DB_DRIVER: Literal["sqlite", "postgresql"] = "postgresql"

    if DB_DRIVER == "sqlite":
        # SQLite数据库链接(异步)
        DB_ASYNC_URL: str = f"sqlite+aiosqlite:///{os.path.join(FASTAPI_BASE_DIR, 'db', 'database.sqlite3')}"

    elif DB_DRIVER == "postgresql":
        # 数据库地址
        DB_POSTGRESQL_HOST: str = "127.0.0.1"
        # 数据库端口
        DB_POSTGRESQL_PORT: int = 5432
        # 数据库名称
        DB_POSTGRESQL_DATABASE: str = "kore_admin"
        # 数据库账号
        DB_POSTGRESQL_USERNAME: str = "postgres"
        # 数据库密码
        DB_POSTGRESQL_PASSWORD: str = "postgres"
        # PostSQL数据库链接(异步)
        DB_ASYNC_URL: str = (
            f"postgresql+asyncpg://{DB_POSTGRESQL_USERNAME}:{DB_POSTGRESQL_PASSWORD}@{DB_POSTGRESQL_HOST}:{DB_POSTGRESQL_PORT}/{DB_POSTGRESQL_DATABASE}"
        )

    DB_PARAMS: Dict[str, Dict[str, Any]] = {
        "sqlite": {
            "echo": False,
        },
        "postgresql": {
            "echo": False,
            "echo_pool": False,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "pool_size": 5,
            "max_overflow": 5,
            "connect_args": {},
        },
    }

    # ================================================== 缓存配置 ==================================================

    # 环境启用缓存
    # REDIS_ENABLE: bool = True
    # 缓存服务地址
    # REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    # 缓存服务端口
    # REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    # 缓存服务密码
    # REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    # AUTH 为 True 时需要进行 用户认证
    # REDIS_AUTH = (os.getenv('REDIS_AUTH', 'True') == 'True')
    # 是否对查询结果进行编码处理
    # REDIS_DECODE_RESPONSES = (os.getenv('REDIS_DECODE_RESPONSES', 'True') == 'True')

    # ================================================== 跨域配置 ==================================================

    """
    跨域解决
    详细解释: https://cloud.tencent.com/developer/article/1886114
    官方文档: https://fastapi.tiangolo.com/tutorial/cors/
    """
    # 是否启用跨域
    CORS_ORIGIN_ENABLE: bool = True
    # 只允许访问的域名列表，* 代表所有
    CORS_ALLOW_ORIGINS: list = ["*"]
    # 是否支持携带 cookie
    CORS_ALLOW_CREDENTIALS: bool = True
    # 设置允许跨域的http方法，比如 get、post、put等。
    CORS_ALLOW_METHODS: list = ["*"]
    # 允许携带的headers，可以用来鉴别来源等作用。
    CORS_ALLOW_HEADERS: list = ["*"]

    # ================================================== 邮件配置 ==================================================

    # 邮寄者
    # MAIL_MAILER = os.getenv('MAIL_MAILER', 'smtp')
    # 邮件服务
    # MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.163.com')
    # 邮件端口
    # MAIL_PORT = os.getenv('MAIL_PORT', 465)
    # 邮件SSL证书
    # MAIL_USE_SSL = (os.getenv('DB_DEBUG', 'True') == 'True')
    # 授权邮箱用户名
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    # 授权邮箱授权码
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    # 邮件加密串
    # MAIL_ENCRYPTION = os.getenv('MAIL_ENCRYPTION', '')
    # 邮件发件人名称
    # MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME', '')
    # 邮件发件人地址
    # MAIL_FROM_ADDRESS = os.getenv('MAIL_FROM_ADDRESS', '')


@lru_cache()
def get_settings() -> Settings:
    """获取全局配置"""
    return Settings()


settings = get_settings()
