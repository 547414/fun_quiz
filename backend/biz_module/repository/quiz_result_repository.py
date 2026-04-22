from typing import Optional, List
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from biz_module.entity.quiz_result import QuizResultEntity
from biz_module.model.quiz_result_model import (
    QuizResultModel, QuizResultViewModel, HistoryItemViewModel, OutcomeDistributionModel
)


class QuizResultRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: QuizResultModel):
        return self.add(
            model=model,
            entity=QuizResultEntity
        )

    def update(self, model: QuizResultModel):
        return self.update_entity(
            entity=QuizResultEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_id(self, result_id: str) -> Optional[QuizResultModel]:
        sql = """
        SELECT * FROM bt_quiz_result WHERE id = :result_id
        """
        return self.get_by_params(
            sql=sql,
            model=QuizResultModel,
            params={
                "result_id": result_id
            }
        )

    def get_by_token_id(self, token_id: str) -> Optional[QuizResultModel]:
        sql = """
        SELECT * FROM bt_quiz_result WHERE token_id = :token_id ORDER BY created_at DESC LIMIT 1
        """
        return self.get_by_params(
            sql=sql,
            model=QuizResultModel,
            params={
                "token_id": token_id
            }
        )

    def has_history(self, token_id: str) -> bool:
        sql = """
        SELECT COUNT(*) AS cnt FROM bt_quiz_result WHERE token_id = :token_id
        """
        from basic.model.basic_model import BasisModel
        class _Cnt(BasisModel):
            cnt: int = 0
        row = self.get_by_params(sql=sql, model=_Cnt, params={"token_id": token_id})
        return (row.cnt > 0) if row else False

    def get_history_page(self, token_id: str, search: str, page_index: int, page_size: int):
        where = """
        WHERE r.token_id = :token_id
        """
        query_params = {"token_id": token_id}
        if search:
            where += """
            AND (q.name ILIKE :search OR o.name ILIKE :search OR o.summary ILIKE :search)
            """
            query_params["search"] = f"%{search}%"
        sql = f"""
        SELECT
            r.id AS result_id,
            r.quiz_id,
            q.name AS quiz_name,
            q.quiz_type,
            r.outcome_code,
            o.name AS outcome_name,
            o.summary AS outcome_summary,
            o.avatar AS outcome_avatar,
            r.score,
            r.created_at
        FROM bt_quiz_result r
        LEFT JOIN bt_quiz q ON q.id = r.quiz_id
        LEFT JOIN bt_quiz_outcome o ON o.quiz_id = r.quiz_id AND o.code = r.outcome_code
        {where}
        ORDER BY r.created_at DESC
        """
        return self.get_page(
            sql=sql,
            data_model=HistoryItemViewModel,
            page_index=page_index,
            page_size=page_size,
            params=query_params,
        )

    def get_result_view(self, result_id: str) -> Optional[QuizResultViewModel]:
        sql = """
        SELECT
            r.id AS result_id,
            r.quiz_id,
            q.name AS quiz_name,
            q.quiz_type,
            q.result_config,
            r.outcome_code,
            o.name AS outcome_name,
            o.summary AS outcome_summary,
            o.detail AS outcome_detail,
            o.tags AS outcome_tags,
            o.avatar AS outcome_avatar,
            r.score,
            r.calc_result,
            r.share_image
        FROM bt_quiz_result r
        LEFT JOIN bt_quiz q ON q.id = r.quiz_id
        LEFT JOIN bt_quiz_outcome o ON o.quiz_id = r.quiz_id AND o.code = r.outcome_code
        WHERE r.id = :result_id
        """
        return self.get_by_params(
            sql=sql,
            model=QuizResultViewModel,
            params={
                "result_id": result_id
            }
        )

    def get_outcome_distribution(self, quiz_id: str) -> List[OutcomeDistributionModel]:
        sql = """
        SELECT r.outcome_code, o.name AS outcome_name, COUNT(*) AS cnt
        FROM bt_quiz_result r
        LEFT JOIN bt_quiz_outcome o ON o.quiz_id = r.quiz_id AND o.code = r.outcome_code
        WHERE r.quiz_id = :quiz_id
        GROUP BY r.outcome_code, o.name
        ORDER BY cnt DESC
        """
        return self.get_all_by_params(
            sql=sql,
            model=OutcomeDistributionModel,
            params={
                "quiz_id": quiz_id
            }
        )
