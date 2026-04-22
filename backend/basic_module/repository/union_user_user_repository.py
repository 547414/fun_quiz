from sqlalchemy.orm import Session
from typing import Optional

from basic.repository.base_repository import BaseRepository
from basic_module.entity.union_user_user import UnionUserUserEntity
from basic_module.model.union_user_user_model import UnionUserUserModel


class UnionUserUserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: UnionUserUserModel):
        return self.add(
            model=model,
            entity=UnionUserUserEntity
        )

    def update(self, model: UnionUserUserModel):
        return self.update_entity(
            entity=UnionUserUserEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=UnionUserUserEntity,
            entity_id=data_id
        )

    def get_exist(self, wx_user_id: str):
        sql = """
        SELECT * FROM ct_union_user_user WHERE union_user_user_id = :wx_user_id
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserUserModel,
            params={
                'wx_user_id': wx_user_id
            }
        )

    def get_web_user_exist(self, web_user_id: str):
        sql = """
        SELECT * FROM ct_union_user_user WHERE union_user_user_id = :web_user_id
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserUserModel,
            params={
                'web_user_id': web_user_id
            }
        )

    def get_wx_user_exist(self, wx_user_id: str):
        sql = """
        SELECT * FROM ct_union_user_user WHERE union_user_user_id = :wx_user_id
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserUserModel,
            params={
                'wx_user_id': wx_user_id
            }
        )

    def get_wx_user(self, union_user_id: str):
        sql = """
        SELECT cu.*, cw.id as wx_user_id
        FROM ct_union_user_user cu
        INNER JOIN ct_wx_user cw ON cu.union_user_user_id = cw.id
        WHERE union_user_id = :union_user_id
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserUserModel,
            params={
                'union_user_id': union_user_id
            }
        )

    def get_union_user_user_exist(
            self,
            union_user_id: str,
            union_user_user_category: str,
    ) -> Optional[UnionUserUserModel]:
        sql = """
        SELECT * FROM ct_union_user_user WHERE union_user_id = :union_user_id
        AND union_user_user_category = :union_user_user_category
        """
        return self.get_by_params(
            sql=sql,
            model=UnionUserUserModel,
            params={
                'union_user_id': union_user_id,
                'union_user_user_category': union_user_user_category
            }
        )

    def list_by_union_user_id(self, union_user_id: str):
        sql = """
        SELECT * FROM ct_union_user_user WHERE union_user_id = :union_user_id
        """
        return self.get_all_by_params(
            sql=sql,
            model=UnionUserUserModel,
            params={
                'union_user_id': union_user_id
            }
        )
