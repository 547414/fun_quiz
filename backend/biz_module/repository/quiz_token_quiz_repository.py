from typing import List, Optional, Set
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from biz_module.entity.quiz_token_quiz import QuizTokenQuizEntity
from biz_module.model.quiz_token_model import QuizTokenQuizModel


class QuizTokenQuizRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def delete_by_id(self, data_id: str):
        self.delete(
            entity_id=data_id,
            entity=QuizTokenQuizEntity
        )

    def insert_batch(self, token_id: str, quiz_ids: List[str]):
        for quiz_id in quiz_ids:
            self.add(
                model=QuizTokenQuizModel(
                    token_id=token_id,
                    quiz_id=quiz_id
                ),
                entity=QuizTokenQuizEntity
            )

    def delete_by_token_id(self, token_id: str):
        sql = """
        SELECT id, token_id, quiz_id FROM bt_quiz_token_quiz WHERE token_id = :token_id
        """
        rows = self.get_all_by_params(
            sql=sql,
            model=QuizTokenQuizModel,
            params={
                "token_id": token_id
            }
        )
        for row in rows:
            self.delete_by_id(
                data_id=row.id
            )

    def get_quiz_ids_by_token(self, token_id: str) -> Optional[Set[str]]:
        """返回该 token 授权的测验 ID 集合，无记录则返回 None（表示不限制）"""
        sql = """
        SELECT id, token_id, quiz_id FROM bt_quiz_token_quiz WHERE token_id = :token_id
        """
        rows = self.get_all_by_params(
            sql=sql,
            model=QuizTokenQuizModel,
            params={
                "token_id": token_id
            }
        )
        if not rows:
            return None
        return {r.quiz_id for r in rows}
