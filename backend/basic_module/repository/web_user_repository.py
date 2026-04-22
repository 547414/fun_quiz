from typing import Optional

from sqlalchemy.orm import Session

from basic.model.page_sort_model import EnumPageSortModel
from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from basic_module.entity.web_user import UserEntity
from basic_module.model.role_model import EnumRoleCode, EnumRoleScope
from basic_module.model.union_user_model import UnionUserInfoModel
from basic_module.model.union_user_user_model import EnumUnionUserCategory
from basic_module.model.web_user_model import WebUserModel, WebUserViewModel, WebUserPageViewModel, WebUserDetailModel, \
    UserPageParamsModel, UserListParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel


class WebUserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: WebUserModel):
        return self.add(
            model=model,
            entity=UserEntity
        )

    def update(self, model: WebUserModel):
        return self.update_entity(
            entity=UserEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=UserEntity,
            entity_id=data_id
        )

    def get_by_name(self, name: str) -> Optional[WebUserModel]:
        sql = """
        SELECT * FROM ct_web_user WHERE name = :name
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "name": name
            }
        )

    def get_by_id(self, user_id: str) -> Optional[WebUserModel]:
        sql = """
        SELECT * FROM ct_web_user WHERE id = :user_id
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "user_id": user_id
            }
        )

    def get_exist_by_name(
            self,
            user_id: str,
            user_name: str
    ) -> Optional[WebUserModel]:
        sql = """
        SELECT * FROM ct_web_user WHERE name = :user_name AND id != :user_id
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "user_id": user_id,
                "user_name": user_name
            }
        )

    def get_info(self, user_id: str) -> Optional[WebUserViewModel]:
        sql = """
        WITH role_list AS (
        SELECT ct.id AS user_id, cr.name AS role_name, cr.code AS role_code
        FROM ct_web_user ct
        INNER JOIN ct_user_role cur ON cur.user_id = ct.id
        INNER JOIN ct_role cr ON cr.id = cur.role_id
        WHERE ct.id = :user_id
        ORDER BY cr.seq
        ),
        user_info AS (
        SELECT ct.*, JSON_AGG(rl) AS role_list
        FROM ct_web_user ct
        INNER JOIN role_list rl ON rl.user_id = ct.id
        GROUP BY ct.id
        )
        SELECT ui.*, 
        ui.role_list -> 0 ->> 'role_name' AS role_name,
        ui.role_list -> 0 ->> 'role_code' AS role_code
        FROM user_info ui
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserViewModel,
            params={
                "user_id": user_id
            }
        )

    def get_union_user_by_user_id(self, user_id: str):
        sql = """
        WITH union_user AS (
        SELECT cu.*, cuu.union_user_user_id
        FROM ct_union_user cu
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_id = cu.id
        WHERE cuu.union_user_user_id = :user_id
        )
        ,organization_list AS(
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS organization_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_organization cwo ON cwo.web_user_id = cwu.id
        INNER JOIN view_organization_tree vt ON vt.id = cwo.organization_id
        INNER JOIN union_user uu ON uu.union_user_user_id = cwu.id
        GROUP BY cwu.id
        )
        , dept_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS dept_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_dept cwd ON cwd.web_user_id = cwu.id
        INNER JOIN view_dept_tree vt ON vt.id = cwd.dept_id
        INNER JOIN union_user uu ON uu.union_user_user_id = cwu.id
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
        INNER JOIN union_user uu ON uu.id = cu.id
        LEFT JOIN web_user_organization_and_dept_info wuoadi ON wuoadi.web_user_id = cuu.union_user_user_id
        WHERE cu.is_deleted IS FALSE
        GROUP BY cu.id, cu.name
        """

        return self.get_by_params(
            sql=sql,
            model=UnionUserInfoModel,
            params={
                "user_id": user_id
            }
        )

    def get_detail(self, user_id: str) -> Optional[WebUserDetailModel]:
        sql = """
        WITH role_list AS (
        SELECT ct.id AS user_id,
        JSON_AGG(JSON_BUILD_OBJECT('role_name', cr.name, 'role_code', cr.code) ORDER BY cr.seq) AS role_list
        FROM ct_web_user ct
        INNER JOIN ct_user_role cur ON cur.user_id = ct.id
        INNER JOIN ct_role cr ON cr.id = cur.role_id
        GROUP BY ct.id
        )
        , web_user_organization_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS organization_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_organization cwo ON cwo.web_user_id = cwu.id
        INNER JOIN view_organization_tree vt ON vt.id = cwo.organization_id
        WHERE cwu.id = :user_id
        GROUP BY cwu.id
        )
        , web_user_dept_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS dept_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_dept cwd ON cwd.web_user_id = cwu.id
        INNER JOIN view_dept_tree vt ON vt.id = cwd.dept_id
        WHERE cwu.id = :user_id
        GROUP BY cwu.id
        )
        SELECT ct.*, rl.role_list,
        cu.id AS union_user_uuid, cu.name AS union_user_name,
        wuol.organization_list, wuld.dept_list
        FROM ct_web_user ct
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = ct.id
        INNER JOIN ct_union_user cu ON cu.id = cuu.union_user_id
        INNER JOIN role_list rl ON rl.user_id = ct.id
        LEFT JOIN web_user_organization_list wuol ON wuol.id = ct.id
        LEFT JOIN web_user_dept_list wuld ON wuld.id = ct.id
        WHERE ct.id = :user_id
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserDetailModel,
            params={
                "user_id": user_id
            }
        )

    def get_user_page(
            self,
            params: UserPageParamsModel,
            current_user_info: ValidateTokenResModel
    ) -> Pagination:
        current_role_code = current_user_info.current_user.current_role_code
        permission_role_code_list = [role.value for role in EnumRoleCode]
        if current_role_code != EnumRoleCode.SUPER_ADMIN.value:
            permission_role_code_list.remove(EnumRoleCode.SUPER_ADMIN.value)

        current_role_code = None
        for user in current_user_info.union_user_info.user_list:
            if user.union_user_user_category == EnumUnionUserCategory.WEB_USER.value:
                current_role_code = user.current_role_code
        admin_list = EnumRoleScope.PEOPLE_MANAGE.value

        sql = """
        WITH role_list AS (
        SELECT ct.id AS user_id,
        JSON_AGG(JSON_BUILD_OBJECT('role_name', cr.name, 'role_code', cr.code) ORDER BY cr.seq) AS role_list,
        ARRAY_AGG(cr.code::TEXT) AS role_code_list
        FROM ct_web_user ct
        INNER JOIN ct_user_role cur ON cur.user_id = ct.id
        INNER JOIN ct_role cr ON cr.id = cur.role_id
        GROUP BY ct.id
        )
        , organization_list AS(
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS organization_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_organization cwo ON cwo.web_user_id = cwu.id
        INNER JOIN view_organization_tree vt ON vt.id = cwo.organization_id
        GROUP BY cwu.id
        )
        , dept_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS dept_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_dept cwd ON cwd.web_user_id = cwu.id
        INNER JOIN view_dept_tree vt ON vt.id = cwd.dept_id
        GROUP BY cwu.id
        )
        SELECT ct.*, rl.role_list,
        cu.id AS union_user_uuid, cu.name AS union_user_name,
        ol.organization_list, dl.dept_list
        FROM ct_web_user ct
        INNER JOIN role_list rl ON rl.user_id = ct.id
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = ct.id
        INNER JOIN ct_union_user cu ON cu.id = cuu.union_user_id
        LEFT JOIN organization_list ol ON ol.id = ct.id
        LEFT JOIN dept_list dl ON dl.id = ct.id
        WHERE rl.role_code_list && :role_code_list
        AND NOT EXISTS (
            SELECT unnest(rl.role_code_list)
            EXCEPT
            SELECT unnest(:permission_role_code_list)
        )
        """

        if current_role_code not in admin_list:
            sql += """
            AND cu.id = :self_union_user_id
            """

        if params.search:
            sql += """
            AND (ct.name LIKE :search OR ct.mobile LIKE :search OR ct.email LIKE :search)
            """
        if params.name_sort:
            if params.name_sort.value == EnumPageSortModel.ASC.value:
                sql += """
                ORDER BY ct.name ASC
                """

            if params.name_sort.value == EnumPageSortModel.DESC.value:
                sql += """
                ORDER BY ct.name DESC
                """

        return self.get_page(
            sql=sql,
            data_model=WebUserPageViewModel,
            page_index=params.page_index,
            page_size=params.page_size,
            search=None,
            search_fields=None,
            params={
                "role_code_list": params.role_code_list,
                "permission_role_code_list": permission_role_code_list,
                "self_union_user_id": current_user_info.union_user_info.id,
                "search": f"%{params.search}%"
            }
        )

    def get_by_id_list(self, params: UserListParamsModel):
        sql = """
        WITH role_list AS (
        SELECT ct.id AS user_id,
        JSON_AGG(JSON_BUILD_OBJECT('role_name', cr.name, 'role_code', cr.code) ORDER BY cr.seq) AS role_list,
        ARRAY_AGG(cr.code::TEXT) AS role_code_list
        FROM ct_web_user ct
        INNER JOIN ct_user_role cur ON cur.user_id = ct.id
        INNER JOIN ct_role cr ON cr.id = cur.role_id
        GROUP BY ct.id
        )
        , organization_list AS(
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS organization_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_organization cwo ON cwo.web_user_id = cwu.id
        INNER JOIN view_organization_tree vt ON vt.id = cwo.organization_id
        GROUP BY cwu.id
        )
        , dept_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS dept_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_dept cwd ON cwd.web_user_id = cwu.id
        INNER JOIN view_dept_tree vt ON vt.id = cwd.dept_id
        GROUP BY cwu.id
        )
        SELECT ct.*, rl.role_list,
        cu.id AS union_user_uuid, cu.name AS union_user_name,
        ol.organization_list, dl.dept_list
        FROM ct_web_user ct
        INNER JOIN role_list rl ON rl.user_id = ct.id
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = ct.id
        INNER JOIN ct_union_user cu ON cu.id = cuu.union_user_id
        LEFT JOIN organization_list ol ON ol.id = ct.id
        LEFT JOIN dept_list dl ON dl.id = ct.id
        WHERE ct.id = ANY(:user_id_list)
        """

        return self.get_all_by_params(
            sql=sql,
            model=WebUserPageViewModel,
            params={
                "user_id_list": params.user_id_list,
            }
        )

    def get_user_by_wecom_user_uuid(self, wecom_user_uuid: str):
        sql = """
        SELECT ct.*
        FROM ct_web_user ct
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = ct.id
        WHERE cuu.union_user_user_id = :wecom_user_uuid
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "wecom_user_uuid": wecom_user_uuid
            }
        )

    def get_user_by_union_user_id(
            self,
            union_user_id: str
    ):
        sql = """
        SELECT ct.*
        FROM ct_web_user ct
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = ct.id
        WHERE cuu.union_user_id = :union_user_id
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "union_user_id": union_user_id
            }
        )

    def get_all_wecom_user(self):
        sql = """
        SELECT cwu.*, cwd.id AS wecom_dept_id
        FROM ct_wecom_user cwu
        INNER JOIN  ct_wecom_dept cwd ON cwd.dept_id = ANY(cwu.department_ids)
        """

        return self.get_all_by_params(
            sql=sql,
            model=WecomUserModel,
            params={}
        )

    def get_by_wecom_user_id(self, wecom_user_id: str):
        sql = """
        WITH union_user AS (
        SELECT cuu.union_user_id
        FROM ct_wecom_user cwu
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = cwu.id
        WHERE cuu.union_user_user_id = :wecom_user_id
        )
        SELECT cwu.*
        FROM ct_web_user cwu
        INNER JOIN ct_union_user_user cuu ON cuu.union_user_user_id = cwu.id
        INNER JOIN union_user uu ON uu.union_user_id = cuu.union_user_id
        """
        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "wecom_user_id": wecom_user_id
            }
        )

    def get_organization_and_dept(self, web_user_id: str):
        sql = """
        WITH organization_list AS(
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS organization_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_organization cwo ON cwo.web_user_id = cwu.id
        INNER JOIN view_organization_tree vt ON vt.id = cwo.organization_id
        WHERE cwu.id = :web_user_id
        GROUP BY cwu.id
        )
        , dept_list AS (
        SELECT cwu.id, JSON_AGG(JSON_BUILD_OBJECT(
        'id',vt.id, 'name', vt.name, 'name_list', vt.name_list
        )) AS dept_list
        FROM ct_web_user cwu
        INNER JOIN ct_web_user_dept cwd ON cwd.web_user_id = cwu.id
        INNER JOIN view_dept_tree vt ON vt.id = cwd.dept_id
        WHERE cwu.id = :web_user_id
        GROUP BY cwu.id
        )
        SELECT ol.id AS web_user_id,
        ol.organization_list, dl.dept_list
        FROM organization_list ol
        LEFT JOIN dept_list dl ON dl.id = ol.id
        """
        return self.get_by_params(
            sql=sql,
            model=WebUserModel,
            params={
                "web_user_id": web_user_id
            }
        )
