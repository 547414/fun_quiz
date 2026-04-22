from typing import List

from basic_module.model.permission_assign_model import PermissionAssignModel, EnumPermissionAssignPolicy
from basic_module.repository.permission_assign_repository import PermissionAssignRepository


class PermissionAssignService:
    def __init__(
            self,
            permission_assign_repository: PermissionAssignRepository,
    ):
        self.__permission_assign_repository = permission_assign_repository

    def edit(self, permission_id: str, assign_list: List[PermissionAssignModel]):
        exist_assign_list = self.__permission_assign_repository.get_by_permission_id(
            permission_id=permission_id
        )
        for assign in exist_assign_list:
            self.__permission_assign_repository.delete_by_id(
                permission_assign_id=assign.id
            )
        for item in assign_list:
            item.permission_id = permission_id
            self.__permission_assign_repository.insert(
                model=item
            )

    def delete_by_permission_id(self, permission_id: str):
        exist_assign_list = self.__permission_assign_repository.get_by_permission_id(
            permission_id=permission_id
        )
        for assign in exist_assign_list:
            self.__permission_assign_repository.delete_by_id(
                permission_assign_id=assign.id
            )
