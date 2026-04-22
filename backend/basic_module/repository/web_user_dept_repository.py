from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.web_user_dept import WebUserDeptEntity
from basic_module.model.web_user_dept_model import WebUserDeptModel


class WebUserDeptRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: WebUserDeptModel):
        return self.add(
            model=model,
            entity=WebUserDeptEntity
        )

    def update(self, model: WebUserDeptModel):
        return self.update_entity(
            entity=WebUserDeptEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=WebUserDeptEntity,
            entity_id=data_id
        )

    def get_exist(
            self,
            web_user_id: str,
            dept_id: str
    ):
        sql = """
        SELECT * FROM ct_web_user_dept
        WHERE web_user_id = :web_user_id
        AND dept_id = :dept_id
        """

        return self.get_by_params(
            sql=sql,
            model=WebUserDeptModel,
            params={
                'web_user_id': web_user_id,
                'dept_id': dept_id
            }
        )

    def get_list_by_web_user_id(
            self,
            web_user_id: str
    ):
        sql = """
        SELECT * FROM ct_web_user_dept
        WHERE web_user_id = :web_user_id
        """
        return self.get_all_by_params(
            sql=sql,
            model=WebUserDeptModel,
            params={
                'web_user_id': web_user_id
            }
        )
