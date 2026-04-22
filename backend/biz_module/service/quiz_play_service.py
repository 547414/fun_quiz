from basic.error.base_error import BusinessError
from basic.minio_client.minio_client import MinioClient
from basic_module.model.upload_model import UploadResModel
from biz_module.model.quiz_result_model import (
    SubmitAnswersParamsModel, QuizResultModel, QuizPlayViewModel,
    QuizPlayQuestionModel, QuizPlayOptionModel,
    TokenEntryViewModel, HistoryItemViewModel,
)
from biz_module.repository.quiz_repository import QuizRepository
from biz_module.repository.quiz_question_repository import QuizQuestionRepository
from biz_module.repository.quiz_outcome_repository import QuizOutcomeRepository
from biz_module.repository.quiz_result_repository import QuizResultRepository
from biz_module.repository.quiz_token_repository import QuizTokenRepository
from biz_module.service.quiz_token_service import QuizTokenService
from biz_module.utils.quiz_algo.vector_algo import VectorAlgo
from biz_module.utils.quiz_algo.score_algo import ScoreAlgo
from biz_module.utils.quiz_algo.branch_algo import BranchAlgo
from biz_module.utils.quiz_algo.random_algo import RandomAlgo


ALGO_MAP = {
    "vector": VectorAlgo(),
    "score": ScoreAlgo(),
    "branch": BranchAlgo(),
    "random": RandomAlgo(),
}


class QuizPlayService:
    def __init__(
        self,
        quiz_repository: QuizRepository,
        quiz_question_repository: QuizQuestionRepository,
        quiz_outcome_repository: QuizOutcomeRepository,
        quiz_result_repository: QuizResultRepository,
        quiz_token_service: QuizTokenService,
        minio_client: MinioClient,
    ):
        self.__quiz_repo = quiz_repository
        self.__question_repo = quiz_question_repository
        self.__outcome_repo = quiz_outcome_repository
        self.__result_repo = quiz_result_repository
        self.__token_service = quiz_token_service
        self.__minio_client = minio_client

    def _fill_upload_url(self, item: UploadResModel):
        if item and item.bucket_name and item.object_name:
            item.url = self.__minio_client.get_file_url(item.bucket_name, item.object_name)

    def get_entry(self, token: str) -> TokenEntryViewModel:
        """入口：返回token状态（不校验次数，让前端展示状态）"""
        token_model = self.__token_service.get_detail(token=token)
        has_history = self.__result_repo.has_history(token_id=token_model.id)
        return TokenEntryViewModel(
            status=token_model.status,
            max_uses=token_model.max_uses,
            used_count=token_model.used_count,
            has_history=has_history,
        )

    def get_entry_quizzes(self, token: str, search: str, page_index: int, page_size: int):
        token_model = self.__token_service.get_detail(token=token)
        allowed = self.__token_service.get_allowed_quiz_ids(token_id=token_model.id)
        page = self.__quiz_repo.get_published_page(
            search=search,
            page_index=page_index,
            page_size=page_size,
            allowed_ids=list(allowed) if allowed is not None else None,
        )
        for q in (page.data or []):
            for cover in (q.covers or []):
                self._fill_upload_url(item=cover)
        page.data = [
            {
                "quiz_id": q.id,
                "quiz_name": q.name,
                "quiz_type": q.quiz_type,
                "covers": [c.model_dump() for c in q.covers] if q.covers else None,
                "share_title": q.share_title,
                "share_desc": q.share_desc,
            }
            for q in (page.data or [])
        ]
        return page

    def get_entry_history(self, token: str, search: str, page_index: int, page_size: int):
        token_model = self.__token_service.get_detail(token=token)
        page = self.__result_repo.get_history_page(
            token_id=token_model.id,
            search=search,
            page_index=page_index,
            page_size=page_size,
        )
        for item in (page.data or []):
            self._fill_upload_url(item=item.outcome_avatar)
        return page

    def get_play_data(self, token: str, quiz_id: str) -> QuizPlayViewModel:
        """获取答题所需数据（题目列表，选项不含维度信息）"""
        token_model = self.__token_service.validate_for_play(token=token)
        allowed = self.__token_service.get_allowed_quiz_ids(token_id=token_model.id)
        if allowed is not None and quiz_id not in allowed:
            raise BusinessError("此 Token 无权访问该测验")
        quiz = self.__quiz_repo.get_by_id(quiz_id=quiz_id)
        if not quiz or quiz.status != "published":
            raise BusinessError("测验不可用")

        questions = self.__question_repo.get_by_quiz_id(quiz_id=quiz.id)

        clean_questions = []
        for q in questions:
            clean_options = []
            for opt in q.options:
                clean_options.append(QuizPlayOptionModel(
                    key=opt.key,
                    label=opt.label,
                    images=opt.images,
                    next_question_seq=opt.next_question_seq if quiz.quiz_type == "branch" else None,
                ))
            clean_questions.append(QuizPlayQuestionModel(
                seq=q.seq,
                content=q.content,
                images=q.images,
                is_hidden=q.is_hidden,
                options=clean_options,
                branch_config=q.branch_config if quiz.quiz_type == "branch" else None,
            ))

        for cover in (quiz.covers or []):
            self._fill_upload_url(item=cover)
        for q in clean_questions:
            for img in (q.images or []):
                self._fill_upload_url(item=img)
            for opt in q.options:
                for img in (opt.images or []):
                    self._fill_upload_url(item=img)

        return QuizPlayViewModel(
            quiz_id=quiz.id,
            quiz_name=quiz.name,
            quiz_type=quiz.quiz_type,
            covers=quiz.covers,
            share_title=quiz.share_title,
            questions=clean_questions,
            algo_config=quiz.algo_config if quiz.quiz_type == "branch" else None,
            result_config=quiz.result_config,
        )

    def submit(self, token: str, quiz_id: str, params: SubmitAnswersParamsModel):
        token_model = self.__token_service.validate_for_play(token=token)
        allowed = self.__token_service.get_allowed_quiz_ids(token_id=token_model.id)
        if allowed is not None and quiz_id not in allowed:
            raise BusinessError("此 Token 无权访问该测验")

        quiz = self.__quiz_repo.get_by_id(quiz_id=quiz_id)
        if not quiz or quiz.status != "published":
            raise BusinessError("测验不可用")

        questions = self.__question_repo.get_by_quiz_id(quiz_id=quiz.id)
        outcomes = self.__outcome_repo.get_by_quiz_id(quiz_id=quiz.id)

        algo = ALGO_MAP.get(quiz.quiz_type)
        if not algo:
            raise BusinessError(f"不支持的测验类型: {quiz.quiz_type}")

        calc = algo.calculate(
            answers=params.answers,
            questions=questions,
            outcomes=outcomes,
            algo_config=quiz.algo_config or {},
            special_rules=quiz.special_rules or [],
        )

        outcome = self.__outcome_repo.get_by_code(
            quiz_id=quiz.id,
            code=calc["outcome_code"],
        )
        if not outcome:
            raise BusinessError("结果数据异常")

        result_model = QuizResultModel(
            token_id=token_model.id,
            quiz_id=quiz.id,
            answers=params.answers,
            calc_result=calc.get("calc_result"),
            outcome_code=calc["outcome_code"],
            outcome_id=outcome.id,
            score=calc.get("score"),
        )
        self.__result_repo.insert(model=result_model)

        # 标记本次使用
        self.__token_service.mark_used(token_id=token_model.id)

        latest = self.__result_repo.get_by_token_id(token_id=token_model.id)
        view = self.__result_repo.get_result_view(result_id=latest.id)
        self._fill_upload_url(item=view.outcome_avatar)
        self._fill_upload_url(item=view.share_image)
        return view

    def get_result(self, token: str, result_id: str):
        """通过 result_id 查看结果（验证token有效即可）"""
        # token 必须存在（不校验次数，只要不是完全无效的token）
        token_model = self.__token_service.get_detail(token=token)
        result = self.__result_repo.get_by_id(result_id=result_id)
        if not result or result.token_id != token_model.id:
            raise BusinessError("结果不存在或无权查看")
        view = self.__result_repo.get_result_view(result_id=result_id)
        self._fill_upload_url(item=view.outcome_avatar)
        self._fill_upload_url(item=view.share_image)
        return view
