from typing import List, Optional

from sqlalchemy.orm import Session

from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from basic_module.entity.menu import MenuEntity
from basic_module.model.menu_model import MenuModel, MenuTreeViewModel, MenuMaxModel, MenuViewModel, EnumMenuType, \
    MenuTreeParamsModel, MenuPageParamsModel
from basic_module.model.permission_assign_model import EnumPermissionAssignGrantType, EnumPermissionAssignGranteeType
from basic_module.model.validate_token_model import ValidateTokenResModel


class MenuRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: MenuModel):
        return self.add(
            model=model,
            entity=MenuEntity
        )

    def update(self, model: MenuModel):
        return self.update_entity(
            entity=MenuEntity,
            entity_id=model.id,
            model=model
        )

    def get_menu_tree(self, params: MenuTreeParamsModel) -> Optional[List[MenuTreeViewModel]]:
        sql = """
        SELECT *
        FROM view_menu_tree vt
        WHERE vt.enabled IS TRUE
        """

        if params.parent_id:
            sql += """
            AND :parent_id = ANY(vt.id_list)
            """

        return self.get_all_by_params(
            sql=sql,
            model=MenuTreeViewModel,
            params={
                "parent_id": params.parent_id
            }
        )

    def get_menu_by_code(self, code: str) -> Optional[MenuModel]:
        sql = """
        SELECT * FROM ct_menu WHERE code = :code
        """

        return self.get_by_params(
            sql=sql,
            model=MenuModel,
            params={
                "code": code
            }
        )

    def get_allow_menu_tree(
            self,
            params: MenuTreeParamsModel,
            current_user_info: ValidateTokenResModel
    ) -> Optional[List[MenuTreeViewModel]]:
        sql = """
        WITH permission_assign AS (		
        SELECT DISTINCT UNNEST(vt.id_list) AS menu_id
        FROM view_menu_tree vt
        INNER JOIN ct_permission_assign ca ON ca.grant_object_id = vt.id
        INNER JOIN ct_role cr ON cr.id = ca.grantee_object_id
        WHERE vt.enabled IS TRUE
        AND ca.grant_type::TEXT = :MENU
        AND ca.grantee_type::TEXT = :ROLE_GRANTEE_TYPE
        AND cr.code::TEXT = :role_code
        )
        SELECT vt.*, vt.name AS label, vt.url AS path
        FROM permission_assign pa
        INNER JOIN view_menu_tree vt ON vt.id = pa.menu_id
        """

        if params.parent_id:
            sql += """
            AND :parent_id = ANY(vt.id_list)
            """

        return self.get_all_by_params(
            sql=sql,
            model=MenuTreeViewModel,
            params={
                "parent_id": params.parent_id,
                "MENU": EnumPermissionAssignGrantType.MENU.value,
                "ROLE_GRANTEE_TYPE": EnumPermissionAssignGranteeType.ROLE.value,
                "role_code": current_user_info.current_role_code
            }
        )

    def get_menu_page(
            self,
            params: MenuPageParamsModel,
    ) -> Pagination:
        sql = """
        SELECT *
        FROM view_menu_tree vt
        WHERE vt.enabled IS TRUE
        AND vt.type::TEXT = :NORMAL
        """

        if params.search:
            sql += """
            AND vt.name LIKE :search
            """

        return self.get_page(
            sql=sql,
            data_model=MenuTreeViewModel,
            page_index=params.page_index,
            page_size=params.page_size,
            search=None,
            search_fields=None,
            params={
                "search": f"%{params.search}%",
                "NORMAL": EnumMenuType.NORMAL.value
            }
        )

    def get_by_id(self, menu_id: str) -> Optional[MenuModel]:
        sql = """
        SELECT * FROM ct_menu WHERE id = :menu_id
        """

        return self.get_by_params(
            sql=sql,
            model=MenuModel,
            params={
                "menu_id": menu_id
            }
        )

    def get_max_seq(self, parent_id: Optional[str] = None) -> Optional[MenuMaxModel]:
        sql = """
        SELECT COALESCE(MAX(seq), 0) AS max_seq
        FROM ct_menu
        """

        if parent_id:
            sql += """
            WHERE parent_id = :parent_id
            """

        return self.get_by_params(
            sql=sql,
            model=MenuMaxModel,
            params={
                "parent_id": parent_id
            }
        )

    def get_menu_detail(self, menu_id: str) -> Optional[MenuViewModel]:
        sql = """
        SELECT * FROM view_menu_tree WHERE id = :menu_id
        """

        return self.get_by_params(
            sql=sql,
            model=MenuViewModel,
            params={
                "menu_id": menu_id
            }
        )

    def delete_by_id(self, menu_id: str):
        """
        删除菜单
        :param menu_id: str
        """
        return self.delete(
            entity=MenuEntity,
            entity_id=menu_id
        )

    def get_list(self) -> List[MenuModel]:
        sql = """
        SELECT * FROM ct_menu
        """

        return self.get_all_by_params(
            sql=sql,
            model=MenuModel,
            params={}
        )
