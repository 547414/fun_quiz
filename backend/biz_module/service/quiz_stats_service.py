from basic.error.base_error import BusinessError
from biz_module.model.quiz_model import QuizStatsModel
from biz_module.repository.quiz_repository import QuizRepository
from biz_module.repository.quiz_result_repository import QuizResultRepository


class QuizStatsService:
    def __init__(
        self,
        quiz_repository: QuizRepository,
        quiz_result_repository: QuizResultRepository,
    ):
        self.__quiz_repo = quiz_repository
        self.__result_repo = quiz_result_repository

    def get_stats(self, quiz_id: str) -> QuizStatsModel:
        quiz = self.__quiz_repo.get_by_id(quiz_id=quiz_id)
        if not quiz:
            raise BusinessError("测验不存在")

        distribution = self.__result_repo.get_outcome_distribution(quiz_id=quiz_id)
        participate_count = sum(r.cnt for r in distribution) if distribution else 0

        return QuizStatsModel(
            quiz_id=quiz_id,
            quiz_name=quiz.name,
            total_tokens=0,   # token不再绑定测验，此字段废弃
            used_tokens=participate_count,
            outcome_distribution=[
                {"outcome_code": r.outcome_code, "outcome_name": r.outcome_name, "count": r.cnt}
                for r in distribution
            ] if distribution else [],
        )
