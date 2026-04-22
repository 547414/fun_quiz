from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.web_user_organization import WebUserOrganizationEntity
from basic_module.model.web_user_organization_model import WebUserOrganizationModel


class WebUserOrganizationRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: WebUserOrganizationModel):
        return self.add(
            model=model,
            entity=WebUserOrganizationEntity
        )

    def update(self, model: WebUserOrganizationModel):
        return self.update_entity(
            entity=WebUserOrganizationEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=WebUserOrganizationEntity,
            entity_id=data_id
        )

    def get_exist(
            self,
            web_user_id: str,
            organization_id: str
    ):
        sql = """
        SELECT * FROM ct_web_user_organization
        WHERE web_user_id = :web_user_id
        AND organization_id = :organization_id
        """
        return self.get_by_params(
            sql=sql,
            model=WebUserOrganizationModel,
            params={
                'web_user_id': web_user_id,
                'organization_id': organization_id
            }
        )

    def get_list_by_web_user_id(
            self,
            web_user_id: str
    ):
        sql = """
        SELECT * FROM ct_web_user_organization
        WHERE web_user_id = :web_user_id
        """
        return self.get_all_by_params(
            sql=sql,
            model=WebUserOrganizationModel,
            params={
                'web_user_id': web_user_id
            }
        )
