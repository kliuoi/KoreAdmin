# FastAPI Web应用

这是一个使用FastAPI框架构建的Web应用程序。

## 项目结构

```
.
├── README.md           # 项目说明文件
├── run.py              # 程序入口文件
├── requirements.txt    # 依赖文件
└── server/             # 程序代码目录
    ├── config/         # 环境配置目录
    ├── core/           # 核心代码
    │   └── register/   # 注册全局异常处理和中间件
    ├── db/             # 数据库相关代码
    │   ├── __init__.py # 数据库初始化和会话函数
    │   ├── models.py   # 数据模型
    │   └── database.sqlite3  # SQLite数据库文件
    ├── routers/        # API路由和处理逻辑
    │   ├── __init__.py # 路由include初始化文件
    │   └── system/     # 登录、注册、鉴权等
    ├── static/         # 静态文件目录
    ├── templates/      # 模板文件目录
    └── utils/          # 工具函数和公共代码
        ├── jwt_utils.py    # JWT相关函数
        └── passwd_encrypt.py  # 密码加密相关函数
```

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (数据库)
- Jinja2 (模板引擎)
- Pydantic (设置管理)
- Uvicorn (ASGI服务器)
- Passlib (密码加密)
- Python-jose (JWT)
- Casbin (权限管理)

## 主要功能

1. 用户认证与授权
   - 用户注册
   - 用户登录 (JWT认证)
   - 权限管理

2. 用户管理
   - 用户列表查询
   - 用户信息修改
   - 用户删除

3. API接口
   - RESTful API设计
   - 中间件JWT验证

4. 数据库操作
   - 异步SQLite支持
   - ORM模型定义

5. 配置管理
   - 环境变量配置

6. 异常处理
   - 全局异常处理

## 安装与运行

1. 克隆项目:

```bash
git clone <repository-url>
cd <project-directory>
```

2. 安装依赖:

```bash
pip install -r requirements.txt
```

3. 运行应用:

```bash
python run.py
```

应用将在 `http://localhost:8000` 运行。

## API文档

启动应用后,访问 `http://localhost:8000/docs` 查看Swagger UI API文档。

## 开发注意事项

- 用户认证使用JWT,每个需要认证的API请求都应包含有效的JWT令牌。
- 数据库操作使用SQLAlchemy ORM,确保在进行数据库操作时使用异步方法。
- 所有密码都应该在存储前进行加密。
- 使用Pydantic进行配置管理,确保敏感信息(如数据库连接字符串、JWT密钥)不直接硬编码在代码中。

## 常见问题

Q: 为什么不使用`request.state.user`来存储用户变量?
A: 如果在登录时查询一次用户信息,当用户信息更新后,`user`对象可能不是最新的实例。而每次接口调用时重新查询用户信息的方式,虽然能保证数据最新,但性能开销较大。具体使用哪种方式需要根据实际需求权衡。

## 贡献

欢迎提交问题和拉取请求。对于重大更改,请先开issue讨论您想要更改的内容。

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)
