from typing import Optional

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.organization import OrganizationEntity
from basic_module.model.organization_model import OrganizationTreeParamsModel, OrganizationModel, \
    OrganizationTreeViewModel, OrganizationViewModel


class OrganizationRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: OrganizationModel):
        return self.add(
            model=model,
            entity=OrganizationEntity
        )

    def update(self, model: OrganizationModel):
        return self.update_entity(
            entity=OrganizationEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=OrganizationEntity,
            entity_id=data_id
        )

    def get_organization_tree(
            self,
            params: OrganizationTreeParamsModel,
    ):
        if params.search_value:
            sql = """
            WITH id_list AS (
            SELECT DISTINCT UNNEST(vt.organization_id_list) AS id
            FROM view_organization_tree vt
            WHERE vt.name LIKE :search_value
            )
            , data_list AS (
            SELECT vt.*, (vt.name LIKE :search_value) AS is_matched
            FROM view_organization_tree vt
            INNER JOIN id_list il ON il.id = vt.id
            )
            """
        else:
            sql = """
            WITH data_list AS (
            SELECT * 
            FROM view_organization_tree vt
            )
            """

        sql += """
        SELECT *
        FROM data_list dl
        WHERE TRUE
        """

        if params.level is not None:
            sql += """
            AND dl.level = :level
            """

        if params.parent_id:
            sql += """
            AND dl.parent_id = :parent_id
            """

        if params.level is None and params.parent_id is None:
            sql += """
            AND dl.level = 1
            """

        sql += """
        ORDER BY dl.seq_list
        """
        return self.get_all_by_params(
            sql=sql,
            model=OrganizationTreeViewModel,
            params={
                "level": params.level,
                "parent_id": params.parent_id,
                "search_value": f'%{params.search_value}%'
            }
        )

    def get_by_id(self, organization_id: str) -> Optional[OrganizationModel]:
        sql = """
        SELECT * FROM ct_organization WHERE id = :organization_id
        """
        return self.get_by_params(
            sql=sql,
            model=OrganizationModel,
            params={
                "organization_id": organization_id
            }
        )

    def get_by_name(self, name: str) -> Optional[OrganizationModel]:
        sql = """
        SELECT * FROM ct_organization WHERE name = :name
        """
        return self.get_by_params(
            sql=sql,
            model=OrganizationModel,
            params={
                "name": name
            }
        )

    def get_detail_by_id(self, organization_id: str) -> Optional[OrganizationViewModel]:
        sql = """
        SELECT * FROM view_organization_tree WHERE id = :organization_id
        """
        return self.get_by_params(
            sql=sql,
            model=OrganizationViewModel,
            params={
                "organization_id": organization_id
            }
        )

    def get_by_code(self, code: str):
        sql = """
        SELECT * FROM ct_organization WHERE code = :code
        """
        return self.get_by_params(
            sql=sql,
            model=OrganizationModel,
            params={
                "code": code
            }
        )
