from typing import Optional, List

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.user_role import UserRoleEntity
from basic_module.model.user_role_model import UserRoleModel, EnumUserRoleCategory, UserRoleViewModel


class UserRoleRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: UserRoleModel):
        return self.add(
            model=model,
            entity=UserRoleEntity
        )

    def update(self, model: UserRoleModel):
        return self.update_entity(
            entity=UserRoleEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, user_role_id: str):
        return self.delete(
            entity=UserRoleEntity,
            entity_id=user_role_id
        )

    def get_exist(self, user_id: str, role_code: str):
        sql = """
        SELECT cur.* FROM ct_user_role cur
        INNER JOIN ct_role cr ON cur.role_id = cr.id
        WHERE cur.user_id = :user_id
        AND cr.code = :role_code
        """

        return self.get_by_params(
            sql=sql,
            model=UserRoleModel,
            params={
                'user_id': user_id,
                'role_code': role_code
            }
        )

    def get_exist_list(self, user_id: str):
        sql = """
        SELECT cur.*, cr.code as role_code
        FROM ct_user_role cur
        INNER JOIN ct_role cr ON cur.role_id = cr.id
        WHERE cur.user_id = :user_id
        """

        return self.get_all_by_params(
            sql=sql,
            model=UserRoleViewModel,
            params={
                'user_id': user_id,
            }
        )

    def get_by_user_id(self, user_id: str) -> Optional[List[UserRoleViewModel]]:
        sql = """
        SELECT cur.*, cr.code as role_code
        FROM ct_user_role cur
        INNER JOIN ct_role cr ON cur.role_id = cr.id
        WHERE cur.user_id = :user_id
        """

        return self.get_all_by_params(
            sql=sql,
            model=UserRoleViewModel,
            params={
                'user_id': user_id
            }
        )

    def get_list(
            self,
            user_id: str,
            category: str
    ) -> Optional[List[UserRoleViewModel]]:
        sql = """
        SELECT cur.*, cr.code AS role_code, cr.id AS role_id, cur.user_category, cur.user_id
        FROM ct_user_role cur
        INNER JOIN ct_role cr ON cur.role_id = cr.id
        WHERE cur.user_id = :user_id
        AND cur.user_category::TEXT = :category
        ORDER BY cr.seq
        """

        return self.get_all_by_params(
            sql=sql,
            model=UserRoleViewModel,
            params={
                'user_id': user_id,
                'category': category
            }
        )
