from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from biz_module.entity.quiz import QuizEntity
from biz_module.model.quiz_model import QuizModel, QuizViewModel, QuizListParamsModel, PublishedQuizModel


class QuizRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: QuizModel):
        return self.add(
            model=model,
            entity=QuizEntity
        )

    def update(self, model: QuizModel):
        return self.update_entity(
            entity=QuizEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=QuizEntity,
            entity_id=data_id
        )

    def get_by_id(self, quiz_id: str) -> Optional[QuizModel]:
        sql = """
        SELECT * FROM bt_quiz WHERE id = :quiz_id
        """
        return self.get_by_params(
            sql=sql,
            model=QuizModel,
            params={
                "quiz_id": quiz_id
            }
        )

    def get_by_code(self, code: str) -> Optional[QuizModel]:
        sql = """
        SELECT * FROM bt_quiz WHERE code = :code
        """
        return self.get_by_params(
            sql=sql,
            model=QuizModel,
            params={
                "code": code
            }
        )

    def get_published_list(self) -> List[QuizModel]:
        sql = """
        SELECT * FROM bt_quiz WHERE status = 'published'
        ORDER BY sort_order ASC, created_at DESC
        """
        return self.get_all_by_params(
            sql=sql,
            model=QuizModel,
            params={}
        )

    def get_published_page(self, search: str, page_index: int, page_size: int, allowed_ids: Optional[List[str]] = None):
        where = """
        WHERE status = 'published'
        """
        query_params = {}
        if search:
            where += """
            AND name ILIKE :search
            """
            query_params["search"] = f"%{search}%"
        if allowed_ids is not None:
            where += """
            AND id = ANY(:allowed_ids)
            """
            query_params["allowed_ids"] = allowed_ids
        sql = f"""
        SELECT id, name, quiz_type, covers, share_title, share_desc
        FROM bt_quiz
        {where}
        ORDER BY sort_order ASC, created_at DESC
        """
        return self.get_page(
            sql=sql,
            data_model=PublishedQuizModel,
            page_index=page_index,
            page_size=page_size,
            params=query_params,
        )

    def page(self, params: QuizListParamsModel):
        where = """
        WHERE TRUE
        """
        query_params = {}

        if params.search:
            where += """
            AND (name LIKE :search OR code LIKE :search)
            """
            query_params["search"] = f"%{params.search}%"
        if params.quiz_type:
            where += """
            AND quiz_type = :quiz_type
            """
            query_params["quiz_type"] = params.quiz_type
        if params.status:
            where += """
            AND status = :status
            """
            query_params["status"] = params.status

        sql = f"""
        SELECT q.*,
               (SELECT COUNT(*) FROM bt_quiz_question qq WHERE qq.quiz_id = q.id) AS question_count,
               (SELECT COUNT(*) FROM bt_quiz_outcome qo WHERE qo.quiz_id = q.id) AS outcome_count,
               (SELECT COUNT(*) FROM bt_quiz_result qr WHERE qr.quiz_id = q.id) AS participate_count
        FROM bt_quiz q
        {where}
        ORDER BY q.sort_order ASC, q.created_at DESC
        """

        return self.get_page(
            sql=sql,
            data_model=QuizViewModel,
            page_index=params.page_index,
            page_size=params.page_size,
            params=query_params,
        )
