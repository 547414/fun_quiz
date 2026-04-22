from typing import List

from basic.error.base_error import BusinessError
from basic_module.model.menu_model import MenuTreeViewModel
from basic_module.model.organization_model import OrganizationTreeParamsModel, EditOrganizationParamsModel, \
    DeleteOrganizationParamsModel, ChangeOrganizationEnabledParamsModel, SaveOrganizationSeqAndParentModel, \
    OrganizationTreeViewModel
from basic_module.repository.organization_repository import OrganizationRepository
from basic_module.service.tree_service import TreeService


class OrganizationService:
    def __init__(
            self,
            organization_repository: OrganizationRepository,
            tree_service: TreeService
    ):
        self.__organization_repository = organization_repository
        self.__tree_service = tree_service

    def tree(self, params: OrganizationTreeParamsModel):
        tree_list = self.__organization_repository.get_organization_tree(
            params=params
        )
        tree_data = tree_list
        # if len(tree_list) > 1:
        #     tree_data = self.__tree_service.build_tree(tree_list)
        # if len(tree_list) == 1:
        #     tree_data[0].children = []
        return tree_data

    def edit(self, params: EditOrganizationParamsModel):
        if params.id:
            exist = self.__organization_repository.get_by_id(
                organization_id=params.id
            )
            if not exist:
                raise BusinessError('未找到组织信息')
            exist.name = params.name
            exist.code = params.code
            exist.category = params.category
            exist.address = params.address
            exist.parent_id = params.parent_id
            exist.seq = params.seq
            exist.enabled = params.enabled
            self.__organization_repository.update(
                model=exist
            )
        else:
            exist = self.__organization_repository.get_by_name(
                name=params.name
            )
            if exist:
                raise BusinessError('组织已存在')
            self.__organization_repository.insert(
                model=params.to_organization_model()
            )

    def detail(self, organization_id: str):
        exist = self.__organization_repository.get_detail_by_id(
            organization_id=organization_id
        )
        if not exist:
            raise BusinessError('未找到组织信息')
        return exist

    def delete(self, params: DeleteOrganizationParamsModel):
        exist = self.__organization_repository.get_by_id(
            organization_id=params.organization_id
        )
        if not exist:
            raise BusinessError('未找到组织信息')
        self.__organization_repository.delete_by_id(
            data_id=params.organization_id
        )

    def change_enabled(self, params: ChangeOrganizationEnabledParamsModel):
        exist = self.__organization_repository.get_by_id(
            organization_id=params.organization_id
        )
        if not exist:
            raise BusinessError('未找到组织信息')
        exist.enabled = params.enabled
        self.__organization_repository.update(
            model=exist
        )

    def save_seq_and_parent(
            self,
            params: SaveOrganizationSeqAndParentModel,
    ):
        self.do_save_seq_and_parent(
            organization_list=params.organization_tree
        )

    def do_save_seq_and_parent(
            self,
            organization_list: List[OrganizationTreeViewModel]
    ):
        for index, organization in enumerate(organization_list):
            organization_model = self.__organization_repository.get_by_id(
                organization_id=organization.id
            )
            organization_model.seq = organization.seq
            organization_model.parent_id = organization.parent_id
            self.__organization_repository.update(
                model=organization_model
            )
            if organization.children:
                self.do_save_seq_and_parent(
                    organization_list=organization.children
                )
        return True
