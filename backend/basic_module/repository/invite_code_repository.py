from sqlalchemy.orm import Session

from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from basic_module.entity.invite_code import InviteCodeEntity
from basic_module.model.invite_code_model import InviteCodeModel, InviteCodePageParamsModel, InviteCodeStatisticsModel


class InviteCodeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: InviteCodeModel):
        return self.add(
            model=model,
            entity=InviteCodeEntity
        )

    def update(self, model: InviteCodeModel):
        return self.update_entity(
            entity=InviteCodeEntity,
            entity_id=model.id,
            model=model
        )

    def get_company_page(
            self,
            params: InviteCodePageParamsModel,
    ) -> Pagination:
        sql = """
        SELECT *
        FROM ct_invite_code
        WHERE deleted IS FALSE
        """

        if params.search:
            sql += """
            AND brief LIKE :search
            """

        return self.get_page(
            sql=sql,
            data_model=InviteCodeModel,
            page_index=params.page_index,
            page_size=params.page_size,
            search=None,
            search_fields=None,
            params={
                "search": f"%{params.search}%",
            }
        )

    def get_by_id(self, invite_code_id: str):
        sql = """
        SELECT *
        FROM ct_invite_code
        WHERE id = :invite_code_id
        """

        return self.get_by_params(
            sql=sql,
            model=InviteCodeModel,
            params={
                "invite_code_id": invite_code_id
            }
        )

    def get_by_name(self, name: str):
        sql = """
        SELECT *
        FROM ct_invite_code
        WHERE name = :name
        """

        return self.get_by_params(
            sql=sql,
            model=InviteCodeModel,
            params={
                "name": name
            }
        )

    def get_by_code(self, code: str):
        sql = """
        SELECT *
        FROM ct_invite_code
        WHERE code = :code
        """

        return self.get_by_params(
            sql=sql,
            model=InviteCodeModel,
            params={
                "code": code
            }
        )

    def statistics(self):
        sql = """
        WITH data_list AS (
        SELECT cic.id, cic.brief, cic.max_limit, cic.register_num, cic.deadline, cic.enabled
        FROM ct_invite_code cic
        WHERE cic.deleted IS FALSE
        )
        SELECT COUNT(dl.*) AS total, 
        COUNT(dl.*)  FILTER (WHERE dl.max_limit = dl.register_num) AS run_out,
        COUNT(dl.*)  FILTER (WHERE dl.max_limit != dl.register_num) AS not_run_out,
        COUNT(dl.*)  FILTER (WHERE dl.deadline < NOW()) AS expired
        FROM data_list dl
        """

        return self.get_by_params(
            sql=sql,
            model=InviteCodeStatisticsModel,
            params={}
        )
