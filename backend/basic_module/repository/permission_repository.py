from typing import Optional

from sqlalchemy.orm import Session

from basic.model.page_sort_model import EnumPageSortModel
from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from basic_module.entity.permission import PermissionEntity
from basic_module.model.permission_model import PermissionModel, PermissionPageViewModel, PermissionViewModel, \
    PermissionPageParamsModel


class PermissionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: PermissionModel):
        return self.add(
            model=model,
            entity=PermissionEntity
        )

    def update(self, model: PermissionModel):
        return self.update_entity(
            entity=PermissionEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=PermissionEntity,
            entity_id=data_id
        )

    def get_permission_page(
            self,
            params: PermissionPageParamsModel,
    ) -> Pagination:
        sql = """
        SELECT *
        FROM view_permission vp
        WHERE TRUE
        """

        if params.category_list:
            sql += """
            AND vp.resource_category::TEXT = ANY(:category_list)
            """

        if params.search:
            sql += """
            AND vp.name LIKE :search
            """
        if params.name_sort:
            if params.name_sort.value == EnumPageSortModel.ASC.value:
                sql += """
                ORDER BY vp.name ASC
                """
            elif params.name_sort.value == EnumPageSortModel.DESC.value:
                sql += """
                ORDER BY vp.name DESC
                """

        return self.get_page(
            sql=sql,
            data_model=PermissionPageViewModel,
            page_index=params.page_index,
            page_size=params.page_size,
            search=None,
            search_fields=None,
            params={
                "search": f"%{params.search}%",
                "category_list": params.category_list,
            }
        )

    def get_by_id(self, permission_id: str):
        sql = """
        SELECT * FROM ct_permission WHERE id = :permission_id
        """

        return self.get_by_params(
            sql=sql,
            model=PermissionModel,
            params={
                "permission_id": permission_id
            }
        )

    def get_detail_by_id(self, permission_id: str):
        sql = """
        SELECT *
        FROM view_permission vp
        WHERE vp.id = :permission_id
        """

        return self.get_by_params(
            sql=sql,
            model=PermissionViewModel,
            params={
                "permission_id": permission_id
            }
        )

    def get_exist(
            self,
            name: str,
            code: str,
            permission_id: Optional[str] = None,
    ):
        sql = """
        SELECT * FROM ct_permission
        WHERE (code = :code OR name = :name)
        """

        if permission_id:
            sql += """
            AND id != :permission_id
            """

        return self.get_by_params(
            sql=sql,
            model=PermissionModel,
            params={
                "name": name,
                "code": code,
                "permission_id": permission_id,
            }
        )
