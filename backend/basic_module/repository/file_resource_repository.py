from typing import List, Optional

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.file_resource import FileResourceEntity
from basic_module.model.file_resource_model import FileResourceModel


class FileResourceRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: FileResourceModel):
        return self.add(
            model=model,
            entity=FileResourceEntity
        )

    def update(self, model: FileResourceModel):
        return self.update_entity(
            entity=FileResourceEntity,
            entity_id=model.id,
            model=model
        )

    def get_exist(
            self,
            resource_category: str,
            resource_id: str,
            relationship: str
    ) -> Optional[List[FileResourceModel]]:
        sql = """
        SELECT * FROM ct_file_resource
        WHERE resource_category = :resource_category
        AND resource_id = :resource_id
        AND relationship = :relationship
        """
        return self.get_all_by_params(
            sql=sql,
            model=FileResourceModel,
            params={
                "resource_category": resource_category,
                "resource_id": resource_id,
                "relationship": relationship
            }
        )
