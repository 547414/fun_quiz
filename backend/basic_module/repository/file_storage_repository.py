from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.file_storage import FileStorageEntity
from basic_module.model.file_storage_model import FileStorageModel


class FileStorageRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: FileStorageModel):
        return self.add(
            model=model,
            entity=FileStorageEntity
        )

    def update(self, model: FileStorageModel):
        return self.update_entity(
            entity=FileStorageEntity,
            entity_id=model.id,
            model=model
        )

    def get_exist(self, file_hash: str):
        sql = """
        SELECT * 
        FROM ct_file_storage 
        WHERE hash = :file_hash
        """

        return self.get_by_params(
            sql=sql,
            model=FileStorageModel,
            params={
                "file_hash": file_hash
            }
        )
