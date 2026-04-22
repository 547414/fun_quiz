import importlib
import os
import pytest
from app import Container
from basic_module.model.backend_api_model import BackendApiModel
from basic_module.repository.backend_api_repository import BackendApiRepository
from config.config import Config


@pytest.fixture()
def container():
    container = Container()
    container.config.from_dict(Config().model_dump())
    container.wire(packages=[__name__])
    return container


def test_generate_backend_api(
        container: Container
):
    backend_api_repository: BackendApiRepository = (
        container.basic_module_container.backend_api_repository()
    )
    basic_module_container = container.basic_module_container
    uow = basic_module_container.unit_of_work()
    print()
    with uow:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(path, "../")
        blueprints_dir = f"{base_path}app/router"
        for filename in os.listdir(blueprints_dir):
            if filename.endswith('_router.py'):
                module_name = f'app.router.{filename[:-3]}'
                mod = importlib.import_module(module_name)
                if hasattr(mod, 'router'):
                    base_url = f'/api/{filename[:-10]}'
                    # 获取每个模块的所有路由
                    for route in mod.router.routes:
                        url = f"{base_url}{route.path}"
                        print(url)
                        exist = backend_api_repository.get_exist(
                            url=url
                        )
                        if exist:
                            continue
                        backend_api_repository.insert(
                            model=BackendApiModel(
                                url=url,
                                enabled=True,
                                ignore_auth=False
                            )
                        )
