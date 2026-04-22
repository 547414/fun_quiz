from typing import List

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.file_info import FileInfoEntity
from basic_module.model.file_info_model import FileInfoModel, FileInfoViewModel


class FileInfoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: FileInfoModel):
        return self.add(
            model=model,
            entity=FileInfoEntity
        )

    def update(self, model: FileInfoModel):
        return self.update_entity(
            entity=FileInfoEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_ids(self, ids: List[str]):
        sql = """
        SELECT co.id AS file_info_id, co.name AS file_name, cs.bucket_name, cs.object_name AS file_object_name,
        cs.path || '/' || cs.object_name AS object_name, cs.size AS file_size, cs.type AS file_type
        FROM ct_file_info co
        INNER JOIN ct_file_storage cs ON cs.id = co.file_storage_id
        WHERE co.id = ANY(:ids)
        """
        return self.get_all_by_params(
            sql=sql,
            model=FileInfoViewModel,
            params={
                "ids": ids
            }
        )

    def get_by_id(self, file_info_id: str):
        sql = """
        SELECT co.id AS file_info_id, co.name AS file_name, cs.bucket_name, cs.object_name AS file_object_name,
        cs.path || '/' || cs.object_name AS object_name, cs.size AS file_size, cs.type AS file_type
        FROM ct_file_info co
        INNER JOIN ct_file_storage cs ON cs.id = co.file_storage_id
        WHERE co.id = :file_info_id
        """
        return self.get_by_params(
            sql=sql,
            model=FileInfoViewModel,
            params={
                "file_info_id": file_info_id
            }
        )
