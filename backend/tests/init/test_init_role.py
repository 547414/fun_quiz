import pytest
from app import Container
from basic_module.model.role_model import EnumRoleCode, RoleModel
from basic_module.repository.role_repository import RoleRepository
from config.config import Config


@pytest.fixture()
def container():
    container = Container()
    container.config.from_dict(Config().model_dump())
    container.wire(packages=[__name__])
    return container


def test_generate_role(
        container: Container
):
    role_repository: RoleRepository = (
        container.basic_module_container.role_repository()
    )
    basic_module_container = container.basic_module_container
    uow = basic_module_container.unit_of_work()
    print()
    with uow:
        # 根据 EnumRole 生成角色
        for role in EnumRoleCode:
            print(f"generate role: {EnumRoleCode[role.value]}, {role.value}")
            exist = role_repository.get_exist(
                name=str(role),
                code=role.value
            )
            if exist:
                continue
            role_repository.insert(
                model=RoleModel(
                    name=str(role),
                    code=role.value,
                    enabled=True
                )
            )
