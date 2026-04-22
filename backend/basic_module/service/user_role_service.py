from typing import List

from basic_module.model.user_role_model import UserRoleModel, EnumUserRoleCategory
from basic_module.repository.role_repository import RoleRepository
from basic_module.repository.user_role_repository import UserRoleRepository


class UserRoleService:
    def __init__(
            self,
            user_role_repository: UserRoleRepository,
            role_repository: RoleRepository
    ):
        self.__user_role_repository = user_role_repository
        self.__role_repository = role_repository

    def add_user_role(self, user_id: str, role_code_list: List[str]):
        for role_code in role_code_list:
            exist = self.__user_role_repository.get_exist(
                user_id=user_id,
                role_code=role_code
            )
            if not exist:
                role = self.__role_repository.get_by_code(
                    code=role_code
                )
                self.__user_role_repository.insert(
                    model=UserRoleModel(
                        user_id=user_id,
                        role_id=role.id,
                        user_category=EnumUserRoleCategory.WEB_USER.value)
                )

    def edit_user_role(self, user_id: str, role_code_list: List[str]):
        exist_list = self.__user_role_repository.get_by_user_id(
            user_id=user_id,
        )
        if not exist_list:
            self.add_user_role(
                user_id=user_id,
                role_code_list=role_code_list
            )
        else:
            for exist in exist_list:
                self.__user_role_repository.delete_by_id(
                    user_role_id=exist.id
                )

            for role_code in role_code_list:
                role = self.__role_repository.get_by_code(
                    code=role_code
                )
                self.__user_role_repository.insert(
                    model=UserRoleModel(
                        user_id=user_id,
                        role_id=role.id,
                        user_category=EnumUserRoleCategory.WEB_USER.value
                    )
                )

    def get_user_role_list(
            self,
            user_id: str,
            category: str
    ):
        return self.__user_role_repository.get_list(
            user_id=user_id,
            category=category
        )

    def delete_by_user_id(self, user_id: str):
        exist_list = self.__user_role_repository.get_by_user_id(
            user_id=user_id
        )
        if not exist_list:
            exist_list = []
        for exist in exist_list:
            self.__user_role_repository.delete_by_id(
                user_role_id=exist.id
            )
