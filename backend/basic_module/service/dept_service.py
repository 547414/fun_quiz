import uuid
from typing import List, Dict

from basic.error.base_error import BusinessError
from basic_module.model.dept_model import DeptTreeParamsModel, EditDeptParamsModel, \
    DeleteDeptParamsModel, ChangeDeptEnabledParamsModel, SaveDeptSeqAndParentModel, \
    DeptTreeViewModel
from basic_module.repository.dept_repository import DeptRepository
from basic_module.service.tree_service import TreeService


class DeptService:
    def __init__(
            self,
            dept_repository: DeptRepository,
            tree_service: TreeService
    ):
        self.__dept_repository = dept_repository
        self.__tree_service = tree_service

    def tree(self, params: DeptTreeParamsModel):
        return self.__dept_repository.get_dept_tree(
            params=params
        )

    def edit(self, params: EditDeptParamsModel):
        if params.id:
            exist = self.__dept_repository.get_by_id(
                dept_id=params.id
            )
            if not exist:
                raise BusinessError('未找到部门信息')
            exist.organization_id = params.organization_id
            exist.name = params.name
            exist.code = params.code
            exist.category = params.category
            exist.brief = params.brief
            exist.source_category = params.source_category
            exist.id = params.id
            exist.parent_id = params.parent_id
            exist.seq = params.seq
            exist.enabled = params.enabled
            self.__dept_repository.update(
                model=exist
            )
        else:
            exist = self.__dept_repository.get_by_name(
                organization_id=params.organization_id,
                name=params.name,
            )
            if exist:
                raise BusinessError('部门已存在')
            self.__dept_repository.insert(
                model=params.to_dept_model()
            )

    def detail(self, dept_id: str):
        exist = self.__dept_repository.get_detail_by_id(
            dept_id=dept_id
        )
        if not exist:
            raise BusinessError('未找到部门信息')
        return exist

    def delete(self, params: DeleteDeptParamsModel):
        exist = self.__dept_repository.get_by_id(
            dept_id=params.dept_id
        )
        if not exist:
            raise BusinessError('未找到部门信息')
        self.__dept_repository.delete_by_id(
            data_id=params.dept_id
        )

    def change_enabled(self, params: ChangeDeptEnabledParamsModel):
        exist = self.__dept_repository.get_by_id(
            dept_id=params.dept_id
        )
        if not exist:
            raise BusinessError('未找到部门信息')
        exist.enabled = params.enabled
        self.__dept_repository.update(
            model=exist
        )

    def save_seq_and_parent(
            self,
            params: SaveDeptSeqAndParentModel,
    ):
        self.do_save_seq_and_parent(
            dept_list=params.dept_tree
        )

    def do_save_seq_and_parent(
            self,
            dept_list: List[DeptTreeViewModel]
    ):
        for index, dept in enumerate(dept_list):
            dept_model = self.__dept_repository.get_by_id(
                dept_id=dept.id
            )
            dept_model.seq = dept.seq
            dept_model.parent_id = dept.parent_id
            self.__dept_repository.update(
                model=dept_model
            )
            if dept.children:
                self.do_save_seq_and_parent(
                    dept_list=dept.children
                )
        return True
