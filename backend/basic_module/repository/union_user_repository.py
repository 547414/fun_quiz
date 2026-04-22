from typing import Optional, List

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.union_user import UnionUserEntity
from basic_module.model.union_user_model import UnionUserModel, UnionUserInfoModel, UnionUserUserInfoModel


class UnionUserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: UnionUserModel):
        return self.add(
            model=model,
            entity=UnionUserEntity
        )

    def update(self, model: UnionUserModel):
        return self.update_entity(
            entity=UnionUserEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=UnionUserEntity,
            entity_id=data_id
        )

    def get_by_wx_user_id(self, wx_user_id: str):
        sql = """
        SELECT cu.* FROM ct_union_user cu
        INNER JOIN ct_union_user_user cuu ON cu.id = cuu.union_user_id
        WHERE cuu.union_user_user_id = :wx_user_id
        AND cuu.union_user_user_category = 'WX_USER'
        AND cu.is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserModel,
            params={
                'wx_user_id': wx_user_id
            }
        )

    def get_by_web_user_id(self, web_user_id: str):
        sql = """
        SELECT cu.* FROM ct_union_user cu
        INNER JOIN ct_union_user_user cuu ON cu.id = cuu.union_user_id
        WHERE cuu.union_user_user_id = :web_user_id
        AND cu.is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserModel,
            params={
                'web_user_id': web_user_id
            }
        )


    def get_info(self, union_user_id: str):
        sql = """
        SELECT cu.id, cu.name, JSON_AGG(cuu.*) AS user_list
        FROM ct_union_user cu
        INNER JOIN ct_union_user_user cuu ON cu.id = cuu.union_user_id
        WHERE cu.id = :union_user_id
        AND cu.is_deleted IS FALSE
        GROUP BY cu.id, cu.name
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserInfoModel,
            params={
                'union_user_id': union_user_id,
            }
        )

    def get_by_id(self, union_user_id: str):
        sql = """
        SELECT * FROM ct_union_user
        WHERE id = :union_user_id
        """

        return self.get_by_params(
            sql=sql,
            model=UnionUserModel,
            params={
                'union_user_id': union_user_id
            }
        )

    def get_exist_union_user(
            self,
            union_user_user_id: str,
            union_user_user_category: str,
    ) -> Optional[UnionUserModel]:
        sql = """
        SELECT cu.*
        FROM ct_union_user cu
        INNER JOIN ct_union_user_user cuu ON cu.id = cuu.union_user_id
        WHERE cuu.union_user_user_id = :union_user_user_id
        AND cuu.union_user_user_category = :union_user_user_category
        """

        return self.get_by_params(
            sql=sql,
            model=UnionUserModel,
            params={
                'union_user_user_id': union_user_user_id,
                'union_user_user_category': union_user_user_category
            }
        )

    def get_user_info(self, user_id_list: List[str]) -> Optional[UnionUserUserInfoModel]:
        sql = """
        WITH data_list AS (
        SELECT ct.id AS user_id, ct.name, JSON_AGG(JSON_BUILD_OBJECT(
        'role_name',cr.name,'role_code',cr.code
        )ORDER BY cr.seq) AS role_list
        FROM ct_web_user ct
        INNER JOIN ct_user_role cur ON cur.user_id = ct.id
        INNER JOIN ct_role cr ON cr.id = cur.role_id
        WHERE ct.id = ANY(:user_id_list)
        GROUP BY ct.id
        UNION ALL
        SELECT cu.id AS user_id, cu.name, JSON_AGG(JSON_BUILD_OBJECT(
        'role_name',cr.name,'role_code',cr.code
        )ORDER BY cr.seq) AS role_list
        FROM ct_wecom_user cu
        INNER JOIN ct_user_role cur ON cur.user_id = cu.id
        INNER JOIN ct_role cr ON cr.id = cur.role_id
        WHERE cu.id = ANY(:user_id_list)
        GROUP BY cu.id
        )
        SELECT JSON_OBJECT_AGG(dl.user_id, JSON_BUILD_OBJECT(
        'name',dl.name,'role_list',dl.role_list
        )) AS role_data
        FROM data_list dl
        """

        return self.get_by_params(
            sql=sql,
            model=UnionUserUserInfoModel,
            params={
                'user_id_list': user_id_list
            }
        )

    def get_union_user(self, union_user_id: str):
        sql = """
        WITH union_user AS (
        SELECT cu.*
        FROM ct_union_user cu
        WHERE cu.id = :union_user_id
        )
        ,organization_list AS(
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS organization_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_organization cwo ON cwo.web_user_id = cwu.id
        INNER JOIN view_organization_tree vt ON vt.id = cwo.organization_id
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = cwu.id
        INNER JOIN union_user uu ON uu.id = cuu.union_user_id
        GROUP BY cwu.id
        )
        , dept_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS dept_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_dept cwd ON cwd.web_user_id = cwu.id
        INNER JOIN view_dept_tree vt ON vt.id = cwd.dept_id
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = cwu.id
        INNER JOIN union_user uu ON uu.id = cuu.union_user_id
        GROUP BY cwu.id
        )
        , web_user_organization_and_dept_info AS (
        SELECT ol.id AS web_user_id,
        ol.organization_list, dl.dept_list
        FROM organization_list ol
        LEFT JOIN dept_list dl ON dl.id = ol.id
        )
        SELECT cu.id, cu.name,
        JSON_AGG(JSON_BUILD_OBJECT(
        'id', cuu.id,'union_user_id',cuu.union_user_id,'union_user_user_category',cuu.union_user_user_category,
        'union_user_user_id',cuu.union_user_user_id,
        'organization_list',wuoadi.organization_list,'dept_list',wuoadi.dept_list
        )) AS user_list,
        JSON_AGG(cuu.union_user_user_id) AS user_id_list
        FROM ct_union_user cu
        INNER JOIN ct_union_user_user cuu ON cu.id = cuu.union_user_id
        INNER JOIN  union_user uu ON uu.id = cu.id
        LEFT JOIN web_user_organization_and_dept_info wuoadi ON wuoadi.web_user_id = cuu.union_user_user_id
        WHERE cu.is_deleted IS FALSE
        GROUP BY cu.id, cu.name
        """

        return self.get_by_params(
            sql=sql,
            model=UnionUserInfoModel,
            params={
                "union_user_id": union_user_id
            }
        )
