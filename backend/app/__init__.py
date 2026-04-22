import importlib
import logging
import os
import pathlib
from logging.handlers import TimedRotatingFileHandler

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.containers import Container
from config.config import Config

container = Container()
container.config.from_dict(Config().model_dump())


def register_routers(app: FastAPI):
    blueprints_dir = pathlib.Path(__file__).parent / 'router'
    for filename in os.listdir(blueprints_dir):
        if filename.endswith('_router.py'):
            module_name = f'app.router.{filename[:-3]}'
            mod = importlib.import_module(module_name)
            if hasattr(mod, 'router'):
                app.include_router(mod.router, prefix=f'/api/{filename[:-10]}')


def setup_logging():
    log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')

    # 确保日志目录存在
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, 'app.log')

    # 获取根日志记录器
    logger = logging.getLogger()  # 获取根日志记录器，而不是 "uvicorn"
    logger.setLevel(logging.INFO)  # 设置日志级别

    # 移除所有已有的处理器，防止重复输出
    logger.handlers = []

    # 日志文件处理器，按天分割日志文件
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=0, encoding='utf-8')
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setLevel(logging.INFO)  # 设置处理器的日志级别

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 添加文件处理器到记录器
    logger.addHandler(file_handler)

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 手动刷新日志处理器，以确保日志写入文件（可选）
    file_handler.flush()


def create_app() -> FastAPI:
    app = FastAPI()
    app.container = container
    # 创建数据库表
    # BaseEntity.metadata.create_all(bind=container.engine())

    # https://github.com/ets-labs/python-dependency-injector/issues/328#issuecomment-734040664
    container.wire(packages=[__name__])

    # 注册app.blueprints中以 _blueprint.py 结尾的路由
    register_routers(app)
    # app.add_middleware(AuthMiddleware)

    setup_logging()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
