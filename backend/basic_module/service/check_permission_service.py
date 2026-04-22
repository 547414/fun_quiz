from basic.error.base_error import BusinessError
from basic_module.model.role_model import EnumRoleCode
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.repository.web_user_repository import WebUserRepository


class CheckPermissionService:
    def __init__(
            self,
            web_user_repository: WebUserRepository,
    ):
        self.__web_user_repository = web_user_repository

    def only_super_admin(
            self,
            current_user_info: ValidateTokenResModel
    ):
        if current_user_info.user_category != "USER":
            raise BusinessError("没有权限")
        user = self.__web_user_repository.get_info(user_id=current_user_info.res_user_id)
        if not user:
            raise BusinessError("没有权限")
        if user.role_code.value != EnumRoleCode.SUPER_ADMIN.value:
            raise BusinessError("没有权限")
