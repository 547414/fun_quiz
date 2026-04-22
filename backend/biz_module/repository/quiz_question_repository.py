from typing import Optional, List
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from biz_module.entity.quiz_question import QuizQuestionEntity
from biz_module.model.quiz_question_model import QuizQuestionModel


class QuizQuestionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: QuizQuestionModel):
        return self.add(
            model=model,
            entity=QuizQuestionEntity
        )

    def update(self, model: QuizQuestionModel):
        return self.update_entity(
            entity=QuizQuestionEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=QuizQuestionEntity,
            entity_id=data_id
        )

    def get_by_id(self, question_id: str) -> Optional[QuizQuestionModel]:
        sql = """
        SELECT * FROM bt_quiz_question WHERE id = :question_id
        """
        return self.get_by_params(
            sql=sql,
            model=QuizQuestionModel,
            params={
                "question_id": question_id
            }
        )

    def get_by_quiz_id(self, quiz_id: str) -> List[QuizQuestionModel]:
        sql = """
        SELECT * FROM bt_quiz_question WHERE quiz_id = :quiz_id ORDER BY seq ASC
        """
        return self.get_all_by_params(
            sql=sql,
            model=QuizQuestionModel,
            params={
                "quiz_id": quiz_id
            }
        )

    def delete_by_quiz_id(self, quiz_id: str):
        sql = """
        DELETE FROM bt_quiz_question WHERE quiz_id = :quiz_id
        """
        self.execute_sql(
            sql=sql,
            params={
                "quiz_id": quiz_id
            }
        )
