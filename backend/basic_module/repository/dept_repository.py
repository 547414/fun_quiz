from typing import Optional

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.dept import DeptEntity
from basic_module.model.dept_model import DeptTreeParamsModel, DeptModel, \
    DeptTreeViewModel, DeptViewModel, DeptMaxSeqModel


class DeptRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: DeptModel):
        return self.add(
            model=model,
            entity=DeptEntity
        )

    def update(self, model: DeptModel):
        return self.update_entity(
            entity=DeptEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=DeptEntity,
            entity_id=data_id
        )

    def get_dept_tree(
            self,
            params: DeptTreeParamsModel,
    ):
        if params.search_value:
            sql = """
            WITH id_list AS (
            SELECT DISTINCT UNNEST(vt.dept_id_list) AS id
            FROM view_dept_tree vt
            WHERE vt.name LIKE :search_value
            AND vt.organization_id = :organization_id
            )
            , data_list AS (
            SELECT vt.*, (vt.name LIKE :search_value) AS is_matched
            FROM view_dept_tree vt
            INNER JOIN id_list il ON il.id = vt.id
            """
            if params.organization_id:
                sql += """
                WHERE vt.organization_id = :organization_id
                """
        else:
            sql = """
            WITH data_list AS (
            SELECT * 
            FROM view_dept_tree vt
            """
            if params.organization_id:
                sql += """
                WHERE vt.organization_id = :organization_id
                """

        sql += """
        )
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
            model=DeptTreeViewModel,
            params={
                "organization_id": params.organization_id,
                "level": params.level,
                "parent_id": params.parent_id,
                "search_value": f'%{params.search_value}%'
            }
        )

    def get_by_id(self, dept_id: str) -> Optional[DeptModel]:
        sql = """
        SELECT * FROM ct_dept WHERE id = :dept_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptModel,
            params={
                "dept_id": dept_id
            }
        )

    def get_by_name(
            self,
            name: str,
            organization_id: str,
    ) -> Optional[DeptModel]:
        sql = """
        SELECT *
        FROM ct_dept
        WHERE name = :name
        AND organization_id = :organization_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptModel,
            params={
                "organization_id": organization_id,
                "name": name
            }
        )

    def get_detail_by_id(
            self,
            dept_id: str
    ) -> Optional[DeptViewModel]:
        sql = """
        SELECT * FROM view_dept_tree
        WHERE id = :dept_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptViewModel,
            params={
                "dept_id": dept_id
            }
        )

    def get_by_wecom_dept_id(self, wecom_dept_id: int) -> Optional[DeptModel]:
        sql = """
        SELECT cd.*
        FROM ct_dept cd
        INNER JOIN ct_wecom_dept cwd ON cd.source_id = cwd.id
        WHERE cwd.dept_id = :wecom_dept_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptModel,
            params={
                "wecom_dept_id": wecom_dept_id
            }
        )

    def get_exist_by_wecom_dept_id(self, wecom_dept_id: str) -> Optional[DeptModel]:
        sql = """
        SELECT cd.*
        FROM ct_dept cd
        INNER JOIN ct_wecom_dept cwd ON cd.source_id = cwd.id
        WHERE cwd.id = :wecom_dept_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptModel,
            params={
                "wecom_dept_id": wecom_dept_id
            }
        )


    def get_max_seq(self, parent_id: Optional[str]):
        sql = """
        SELECT COALESCE(COUNT(*), 0) AS max_seq
        FROM ct_dept
        WHERE parent_id = :parent_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptMaxSeqModel,
            params={
                "parent_id": parent_id
            }
        )

    def get_by_source_id(
            self,
            organization_id: str,
            source_id: str
    ):
        sql = """
        SELECT * FROM ct_dept
        WHERE source_id = :source_id
        AND organization_id = :organization_id
        """
        return self.get_by_params(
            sql=sql,
            model=DeptModel,
            params={
                "source_id": source_id,
                "organization_id": organization_id
            }
        )
