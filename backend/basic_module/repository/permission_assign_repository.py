from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.permission_assign import PermissionAssignEntity
from basic_module.model.permission_assign_model import PermissionAssignModel


class PermissionAssignRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: PermissionAssignModel):
        return self.add(
            model=model,
            entity=PermissionAssignEntity
        )

    def update(self, model: PermissionAssignModel):
        return self.update_entity(
            entity=PermissionAssignEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_permission_id(self, permission_id: str):
        sql = """
        SELECT *
        FROM ct_permission_assign
        WHERE permission_id = :permission_id
        """

        return self.get_all_by_params(
            sql=sql,
            model=PermissionAssignModel,
            params={
                "permission_id": permission_id
            }
        )

    def delete_by_id(self, permission_assign_id: str):
        return self.delete(
            entity=PermissionAssignEntity,
            entity_id=permission_assign_id
        )

    def get_exist(
            self,
            grant_type: str,
            grant_object_id: str,
            grantee_type: str,
            grantee_object_id: str,
            permission_id: str
    ):
        sql = """
        SELECT *
        FROM ct_permission_assign
        WHERE grant_type = :grant_type
        AND grant_object_id = :grant_object_id
        AND grantee_type = :grantee_type
        AND grantee_object_id = :grantee_object_id
        AND permission_id = :permission_id
        """

        return self.get_by_params(
            sql=sql,
            model=PermissionAssignModel,
            params={
                "grant_type": grant_type,
                "grant_object_id": grant_object_id,
                "grantee_type": grantee_type,
                "grantee_object_id": grantee_object_id,
                "permission_id": permission_id
            }
        )
