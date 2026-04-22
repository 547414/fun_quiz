import uuid

from basic.error.base_error import BusinessError
from basic_module.model.permission_model import EditPermissionModel, ChangePermissionEnabledModel, \
    EnumResourcePermissionCategory, PermissionPageParamsModel, DeletePermissionParamsModel
from basic_module.repository.backend_api_repository import BackendApiRepository
from basic_module.repository.menu_repository import MenuRepository
from basic_module.repository.permission_repository import PermissionRepository
from basic_module.service.permission_assign_service import PermissionAssignService


class PermissionService:
    def __init__(
            self,
            permission_repository: PermissionRepository,
            permission_assign_service: PermissionAssignService,
            menu_repository: MenuRepository,
            backend_api_repository: BackendApiRepository,
    ):
        self.__permission_repository = permission_repository
        self.__permission_assign_service = permission_assign_service
        self.__menu_repository = menu_repository
        self.__backend_api_repository = backend_api_repository

    def get_permission_page(self, params: PermissionPageParamsModel):
        page_data = self.__permission_repository.get_permission_page(
            params=params
        )
        for item in page_data.data:
            item.resource_category_display = str(item.resource_category)

        return page_data

    def get_permission_detail(self, permission_id: str):
        return self.__permission_repository.get_detail_by_id(
            permission_id=permission_id
        )

    def edit(self, params: EditPermissionModel):
        if not params.resource_id:
            if params.resource_category.value == EnumResourcePermissionCategory.MENU.value:
                menu = self.__menu_repository.get_menu_by_code(
                    code=params.code
                )
                params.resource_id = menu.id
            if params.resource_category.value == EnumResourcePermissionCategory.BACKEND_API.value:
                backend_api = self.__backend_api_repository.get_exist(
                    url=params.name
                )
                params.resource_id = backend_api.id

        permission_id = params.id
        if params.id:
            permission = self.__permission_repository.get_by_id(
                permission_id=params.id
            )
            if permission:
                permission.name = params.name
                permission.code = params.code
                permission.resource_category = params.resource_category
                permission.resource_id = params.resource_id
                permission.enabled = params.enabled
                self.__permission_repository.update(
                    model=permission
                )
        else:
            exist_permission = self.__permission_repository.get_exist(
                name=params.name,
                code=params.code,
                permission_id=params.id
            )
            if exist_permission:
                raise BusinessError("名称或编码已存在")
            model_data = params.to_permission_model()
            model_data.id = str(uuid.uuid4())
            permission_id = model_data.id
            self.__permission_repository.insert(
                model=model_data,
            )
        if params.assign_list:
            self.__permission_assign_service.edit(
                permission_id=permission_id,
                assign_list=params.assign_list,
            )

    def change_permission_enabled(
            self,
            params: ChangePermissionEnabledModel
    ):
        permission = self.__permission_repository.get_by_id(
            permission_id=params.id
        )
        permission.enabled = params.enabled
        self.__permission_repository.update(
            model=permission
        )

    def delete(
            self,
            params: DeletePermissionParamsModel
    ):
        permission = self.__permission_repository.get_by_id(
            permission_id=params.permission_id
        )
        if not permission:
            raise BusinessError("未找到权限信息")
        self.__permission_repository.delete_by_id(
            data_id=params.permission_id
        )
        self.__permission_assign_service.delete_by_permission_id(
            permission_id=params.permission_id
        )
