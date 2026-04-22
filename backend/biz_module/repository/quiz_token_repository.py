from typing import Optional
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from biz_module.entity.quiz_token import QuizTokenEntity
from biz_module.model.quiz_token_model import QuizTokenModel, TokenListParamsModel, TokenDetailViewModel


class QuizTokenRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: QuizTokenModel):
        return self.add(
            model=model,
            entity=QuizTokenEntity
        )

    def update(self, model: QuizTokenModel):
        return self.update_entity(
            entity=QuizTokenEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_id(self, token_id: str) -> Optional[QuizTokenModel]:
        sql = """
        SELECT * FROM bt_quiz_token WHERE id = :token_id
        """
        return self.get_by_params(
            sql=sql,
            model=QuizTokenModel,
            params={
                "token_id": token_id
            }
        )

    def get_by_token(self, token: str) -> Optional[QuizTokenModel]:
        sql = """
        SELECT * FROM bt_quiz_token WHERE token = :token
        """
        return self.get_by_params(
            sql=sql,
            model=QuizTokenModel,
            params={
                "token": token
            }
        )

    def page(self, params: TokenListParamsModel):
        where = "WHERE TRUE"
        query_params = {}

        if params.batch_code:
            where += " AND t.batch_code = :batch_code"
            query_params["batch_code"] = params.batch_code
        if params.status:
            where += " AND t.status = :status"
            query_params["status"] = params.status

        sql = f"""
        SELECT t.*,
               ARRAY_AGG(tq.quiz_id) FILTER (WHERE tq.quiz_id IS NOT NULL) AS quiz_ids
        FROM bt_quiz_token t
        LEFT JOIN bt_quiz_token_quiz tq ON t.id = tq.token_id
        {where}
        GROUP BY t.id
        ORDER BY t.created_at DESC
        """

        return self.get_page(
            sql=sql,
            data_model=TokenDetailViewModel,
            page_index=params.page_index,
            page_size=params.page_size,
            params=query_params,
        )
