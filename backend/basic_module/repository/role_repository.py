from typing import List, Optional

from sqlalchemy.orm import Session

from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from basic_module.entity.role import RoleEntity
from basic_module.model.role_model import RoleModel, RolePageParamsModel, RoleStatisticsModel, RoleMaxSeqModel


class RoleRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: RoleModel):
        return self.add(
            model=model,
            entity=RoleEntity
        )

    def update(self, model: RoleModel):
        return self.update_entity(
            entity=RoleEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=RoleEntity,
            entity_id=data_id
        )

    def get_exist(
            self,
            name: str,
            code: str
    ):
        sql = """
        SELECT * FROM ct_role
        WHERE name = :name
        AND code = :code
        """
        return self.get_by_params(
            sql=sql,
            model=RoleModel,
            params={
                "name": name,
                "code": code
            }
        )

    def get_max_seq(self) -> Optional[RoleModel]:
        sql = """
        SELECT MAX(seq) AS max_seq FROM ct_role
        """

        return self.get_by_params(
            sql=sql,
            model=RoleMaxSeqModel,
            params={}
        )

    def role_statistics(self) -> RoleStatisticsModel:
        sql = """
        WITH role_count AS (
        SELECT COUNT(cr.*)  AS total,
        COUNT(cr.enabled IS TRUE OR NULL) AS enabled_count
        FROM ct_role cr
        )
        , newest_date AS (
        SELECT cr.updated_at AS newest_updated_at
        FROM ct_role cr
        ORDER BY cr.updated_at DESC
        LIMIT 1
        )
        SELECT rc.*, rc.total - rc.enabled_count AS disable_count, nd.*
        FROM role_count rc
        CROSS JOIN newest_date nd
        """
        return self.get_by_params(
            sql=sql,
            model=RoleStatisticsModel,
            params={}
        )

    def get_role_page(
            self,
            params: RolePageParamsModel,
    ) -> Pagination:
        sql = """
        SELECT * 
        FROM ct_role cr
        """

        if params.search:
            sql += """
            WHERE cr.name LIKE :search
            """

        return self.get_page(
            sql=sql,
            data_model=RoleModel,
            page_index=params.page_index,
            page_size=params.page_size,
            search=None,
            search_fields=None,
            params={
                "search": f"%{params.search}%"
            }
        )

    def get_by_id(self, role_id: str) -> RoleModel:
        sql = """
        SELECT * FROM ct_role
        WHERE id = :role_id
        """
        return self.get_by_params(
            sql=sql,
            model=RoleModel,
            params={
                "role_id": role_id
            }
        )

    def get_by_code(self, code: str) -> RoleModel:
        sql = """
        SELECT * FROM ct_role
        WHERE code = :code
        """
        return self.get_by_params(
            sql=sql,
            model=RoleModel,
            params={
                "code": code
            }
        )

    def get_list(self) -> Optional[List[RoleModel]]:
        sql = """
        SELECT * FROM ct_role
        """
        return self.get_all_by_params(
            sql=sql,
            model=RoleModel,
            params={}
        )
