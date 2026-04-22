import uuid
from datetime import datetime

import pytest
from app import Container
from basic_module.model.menu_model import EnumMenuType
from basic_module.model.permission_assign_model import PermissionAssignModel, EnumPermissionAssignGrantType, \
    EnumPermissionAssignGranteeType, EnumPermissionAssignPolicy
from basic_module.model.permission_model import EnumResourcePermissionCategory, PermissionModel
from basic_module.repository.menu_repository import MenuRepository
from basic_module.repository.permission_assign_repository import PermissionAssignRepository
from basic_module.repository.permission_repository import PermissionRepository
from basic_module.repository.role_repository import RoleRepository
from config.config import Config


@pytest.fixture()
def container():
    container = Container()
    container.config.from_dict(Config().model_dump())
    container.wire(packages=[__name__])
    return container


def test_generate_menu_permission(
        container: Container
):
    menu_repository: MenuRepository = (
        container.basic_module_container.menu_repository()
    )
    permission_repository: PermissionRepository = (
        container.basic_module_container.permission_repository()
    )
    permission_assign_repository: PermissionAssignRepository = (
        container.basic_module_container.permission_assign_repository()
    )
    role_repository: RoleRepository = (
        container.basic_module_container.role_repository()
    )
    basic_module_container = container.basic_module_container
    uow = basic_module_container.unit_of_work()
    print()
    with uow:
        menu_list = menu_repository.get_list()
        if not menu_list:
            return
        for menu in menu_list:
            if menu.type == EnumMenuType.AGGREGATION.value:
                continue
            code = menu.code
            permission = permission_repository.get_exist(
                name=menu.name,
                code=code
            )
            if not permission:
                permission_id = str(uuid.uuid4())
                permission_model = PermissionModel(
                    id=permission_id,
                    name=menu.name,
                    code=code,
                    resource_category=EnumResourcePermissionCategory.MENU.value,
                    resource_id=menu.id,
                    enabled=True
                )
                permission_repository.insert(
                    model=permission_model
                )
            else:
                permission_id = permission.id
            role_list = role_repository.get_list()
            for role in role_list:
                exist_permission_assign = permission_assign_repository.get_exist(
                    grant_type=EnumPermissionAssignGrantType.MENU.value,
                    grant_object_id=menu.id,
                    grantee_type=EnumPermissionAssignGranteeType.ROLE.value,
                    grantee_object_id=role.id,
                    permission_id=permission_id
                )
                if not exist_permission_assign:
                    permission_assign_repository.insert(
                        model=PermissionAssignModel(
                            grant_type=EnumPermissionAssignGrantType.MENU.value,
                            grant_object_id=menu.id,
                            grantee_type=EnumPermissionAssignGranteeType.ROLE.value,
                            grantee_object_id=role.id,
                            permission_id=permission_id,
                            start_time=datetime.now(),
                            policy=EnumPermissionAssignPolicy.ALLOW.value,
                        )
                    )
