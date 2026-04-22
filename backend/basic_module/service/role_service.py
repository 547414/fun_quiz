from basic.error.base_error import BusinessError
from basic.model.pagination_model import Pagination
from basic_module.model.auth_model import EnumSpace
from basic_module.model.role_model import EnumRoleCode, RolePageParamsModel, ChangeRoleEnabledParamsModel, \
    EditRoleModel, DeleteRoleParamsModel
from basic_module.model.union_user_user_model import EnumUnionUserCategory
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.repository.role_repository import RoleRepository


class RoleService:
    def __init__(
            self,
            role_repository: RoleRepository,
    ):
        self.__role_repository = role_repository

    def role_statistics(self):
        return self.__role_repository.role_statistics()

    def get_role_page(self, params: RolePageParamsModel) -> Pagination:
        return self.__role_repository.get_role_page(params=params)

    def change_enabled(self, params: ChangeRoleEnabledParamsModel):
        role = self.__role_repository.get_by_id(params.id)
        if not role:
            raise BusinessError("角色不存在")
        if role.code == EnumRoleCode.SUPER_ADMIN.value:
            raise BusinessError("禁止修改超级管理员")
        role.enabled = params.enabled
        self.__role_repository.update(
            model=role
        )

    @staticmethod
    def check_is_super_admin(
            space: str = 'WEB',
            current_user_info: ValidateTokenResModel = None
    ):
        passed = False
        if space == EnumSpace.WEB.value:
            for user in current_user_info.union_user_info.user_list:
                if user.union_user_user_category == EnumUnionUserCategory.WEB_USER.value:
                    if user.current_role_code == EnumRoleCode.SUPER_ADMIN.value:
                        passed = True
        elif space == EnumSpace.WECOM.value:
            for user in current_user_info.union_user_info.user_list:
                if user.union_user_user_category == EnumUnionUserCategory.WECOM_USER.value:
                    if user.current_role_code == EnumRoleCode.SUPER_ADMIN.value:
                        passed = True
        if not passed:
            raise BusinessError('禁止此操作, 仅超级管理员可以操作')

    def edit(
            self,
            params: EditRoleModel,
            current_user_info: ValidateTokenResModel,
            space: str = "WEB"
    ):
        self.check_is_super_admin(
            space=space,
            current_user_info=current_user_info
        )
        if params.id:
            role = self.__role_repository.get_by_id(params.id)
            if not role:
                raise BusinessError("角色不存在")
            if role.code == EnumRoleCode.SUPER_ADMIN.value:
                raise BusinessError("禁止修改超级管理员")
            role.name = params.name
            role.brief = params.brief
            role.code = params.code
            role.enabled = params.enabled
            role.seq = params.seq
            self.__role_repository.update(
                model=role
            )
        else:
            exist_role = self.__role_repository.get_exist(
                name=params.name,
                code=params.code
            )
            if exist_role:
                raise BusinessError("角色已存在")
            max_seq_model = self.__role_repository.get_max_seq()
            if max_seq_model is not None:
                params.seq = max_seq_model.max_seq + 1
            else:
                params.seq = 1
            new_role = params.to_role_model()
            self.__role_repository.insert(model=new_role)

    def delete(self, params: DeleteRoleParamsModel):
        role = self.__role_repository.get_by_id(params.role_id)
        if not role:
            raise BusinessError("角色不存在")
        if role.code == EnumRoleCode.SUPER_ADMIN.value:
            raise BusinessError("禁止删除超级管理员")
        self.__role_repository.delete_by_id(params.role_id)
