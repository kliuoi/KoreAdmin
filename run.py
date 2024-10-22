import uvicorn
import click

from server.core.config import settings
from server import create_app, initdb_common


app = create_app()


@click.group(invoke_without_command=True)
@click.pass_context
def shell_cli(context):
    # 没有指定子命令，执行默认动作：启动FastAPI服务
    if context.invoked_subcommand is None:
        print("启动FastAPI服务...")
        uvicorn.run(
            "run:app",
            host=settings.FASTAPI_HOST,
            port=settings.FASTAPI_PORT,
            log_level="info",
            reload=True,
        )


@shell_cli.command()
def initdb():
    print("初始化数据库...")
    initdb_common()


if __name__ == "__main__":
    shell_cli()
