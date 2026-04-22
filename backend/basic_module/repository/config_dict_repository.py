from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.config_dict import ConfigDictEntity
from basic_module.model.config_dict_model import ConfigDictModel


class ConfigDictRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: ConfigDictModel):
        return self.add(
            model=model,
            entity=ConfigDictEntity
        )

    def update(self, model: ConfigDictModel):
        return self.update_entity(
            entity=ConfigDictEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_code(self, code: str):
        sql = """
        SELECT * FROM ct_config_dict WHERE code = :code
        """

        return self.get_by_params(
            sql=sql,
            model=ConfigDictModel,
            params={
                "code": code
            }
        )
