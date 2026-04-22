from typing import Optional, List
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from biz_module.entity.quiz_outcome import QuizOutcomeEntity
from biz_module.model.quiz_outcome_model import QuizOutcomeModel


class QuizOutcomeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: QuizOutcomeModel):
        return self.add(
            model=model,
            entity=QuizOutcomeEntity
        )

    def update(self, model: QuizOutcomeModel):
        return self.update_entity(
            entity=QuizOutcomeEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=QuizOutcomeEntity,
            entity_id=data_id
        )

    def get_by_id(self, outcome_id: str) -> Optional[QuizOutcomeModel]:
        sql = """
        SELECT * FROM bt_quiz_outcome WHERE id = :outcome_id
        """
        return self.get_by_params(
            sql=sql,
            model=QuizOutcomeModel,
            params={
                "outcome_id": outcome_id
            }
        )

    def get_by_quiz_id(self, quiz_id: str) -> List[QuizOutcomeModel]:
        sql = """
        SELECT * FROM bt_quiz_outcome WHERE quiz_id = :quiz_id ORDER BY sort_order ASC
        """
        return self.get_all_by_params(
            sql=sql,
            model=QuizOutcomeModel,
            params={
                "quiz_id": quiz_id
            }
        )

    def get_by_code(self, quiz_id: str, code: str) -> Optional[QuizOutcomeModel]:
        sql = """
        SELECT * FROM bt_quiz_outcome WHERE quiz_id = :quiz_id AND code = :code
        """
        return self.get_by_params(
            sql=sql,
            model=QuizOutcomeModel,
            params={
                "quiz_id": quiz_id,
                "code": code
            }
        )

    def delete_by_quiz_id(self, quiz_id: str):
        sql = """
        DELETE FROM bt_quiz_outcome WHERE quiz_id = :quiz_id
        """
        self.execute_sql(
            sql=sql,
            params={
                "quiz_id": quiz_id
            }
        )
