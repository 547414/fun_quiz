from basic.error.base_error import BusinessError
from basic.minio_client.minio_client import MinioClient
from basic_module.model.upload_model import UploadResModel
from biz_module.model.quiz_model import (
    EditQuizParamsModel, DeleteQuizParamsModel, PublishQuizParamsModel,
    ImportQuizParamsModel, QuizListParamsModel, QuizModel
)
from biz_module.model.quiz_question_model import BatchSaveQuestionsParamsModel, QuizQuestionModel
from biz_module.model.quiz_outcome_model import BatchSaveOutcomesParamsModel, QuizOutcomeModel
from biz_module.repository.quiz_repository import QuizRepository
from biz_module.repository.quiz_question_repository import QuizQuestionRepository
from biz_module.repository.quiz_outcome_repository import QuizOutcomeRepository


class QuizService:
    def __init__(
        self,
        quiz_repository: QuizRepository,
        quiz_question_repository: QuizQuestionRepository,
        quiz_outcome_repository: QuizOutcomeRepository,
        minio_client: MinioClient,
    ):
        self.__quiz_repo = quiz_repository
        self.__question_repo = quiz_question_repository
        self.__outcome_repo = quiz_outcome_repository
        self.__minio_client = minio_client

    def _fill_upload_url(self, item: UploadResModel):
        if item and item.bucket_name and item.object_name:
            item.url = self.__minio_client.get_file_url(item.bucket_name, item.object_name)

    def page(self, params: QuizListParamsModel):
        page = self.__quiz_repo.page(params=params)
        for quiz in (page.data or []):
            for cover in (quiz.covers or []):
                self._fill_upload_url(item=cover)
        return page

    def detail(self, quiz_id: str):
        quiz = self.__quiz_repo.get_by_id(quiz_id=quiz_id)
        if not quiz:
            raise BusinessError("测验不存在")
        for cover in (quiz.covers or []):
            self._fill_upload_url(item=cover)
        return quiz

    def edit(self, params: EditQuizParamsModel):
        if params.id:
            exist = self.__quiz_repo.get_by_id(quiz_id=params.id)
            if not exist:
                raise BusinessError("测验不存在")
            exist.name = params.name
            exist.covers = params.covers
            exist.cover_prompt = params.cover_prompt
            exist.quiz_type = params.quiz_type
            exist.share_title = params.share_title
            exist.share_desc = params.share_desc
            exist.fallback_outcome_code = params.fallback_outcome_code
            exist.algo_config = params.algo_config
            exist.special_rules = params.special_rules
            exist.result_config = params.result_config
            exist.sort_order = params.sort_order
            self.__quiz_repo.update(model=exist)
        else:
            if not params.code:
                raise BusinessError("测验编码不能为空")
            if self.__quiz_repo.get_by_code(code=params.code):
                raise BusinessError("测验编码已存在")
            self.__quiz_repo.insert(model=params.to_quiz_model())

    def delete(self, params: DeleteQuizParamsModel):
        exist = self.__quiz_repo.get_by_id(quiz_id=params.quiz_id)
        if not exist:
            raise BusinessError("测验不存在")
        if exist.status == "published":
            raise BusinessError("已发布的测验不能直接删除，请先归档")
        self.__quiz_repo.delete_by_id(data_id=params.quiz_id)

    def change_status(self, params: PublishQuizParamsModel):
        exist = self.__quiz_repo.get_by_id(quiz_id=params.quiz_id)
        if not exist:
            raise BusinessError("测验不存在")
        if params.status == "published":
            questions = self.__question_repo.get_by_quiz_id(quiz_id=params.quiz_id)
            outcomes = self.__outcome_repo.get_by_quiz_id(quiz_id=params.quiz_id)
            if not questions:
                raise BusinessError("请先配置题目后再发布")
            if not outcomes:
                raise BusinessError("请先配置结果后再发布")
            has_fallback = any(o.is_fallback for o in outcomes)
            if not has_fallback:
                raise BusinessError("请设置至少一个兜底结果后再发布")
        exist.status = params.status
        self.__quiz_repo.update(model=exist)

    def batch_save_questions(self, params: BatchSaveQuestionsParamsModel):
        quiz = self.__quiz_repo.get_by_id(quiz_id=params.quiz_id)
        if not quiz:
            raise BusinessError("测验不存在")
        self.__question_repo.delete_by_quiz_id(quiz_id=params.quiz_id)
        for q in params.questions:
            q.quiz_id = params.quiz_id
            self.__question_repo.insert(model=q.to_question_model())

    def get_questions(self, quiz_id: str):
        questions = self.__question_repo.get_by_quiz_id(quiz_id=quiz_id)
        for q in questions:
            for img in (q.images or []):
                self._fill_upload_url(item=img)
            for opt in (q.options or []):
                for img in (opt.images or []):
                    self._fill_upload_url(item=img)
        return questions

    def batch_save_outcomes(self, params: BatchSaveOutcomesParamsModel):
        quiz = self.__quiz_repo.get_by_id(quiz_id=params.quiz_id)
        if not quiz:
            raise BusinessError("测验不存在")
        self.__outcome_repo.delete_by_quiz_id(quiz_id=params.quiz_id)
        for o in params.outcomes:
            o.quiz_id = params.quiz_id
            self.__outcome_repo.insert(model=o.to_outcome_model())

    def get_outcomes(self, quiz_id: str):
        outcomes = self.__outcome_repo.get_by_quiz_id(quiz_id=quiz_id)
        for o in outcomes:
            self._fill_upload_url(item=o.avatar)
        return outcomes

    def import_from_definition(self, params: ImportQuizParamsModel):
        """从 SKILL.md 格式的 JSON 导入完整测验"""
        definition = params.definition
        meta = definition.get("meta", {})
        code = meta.get("code")
        if not code:
            raise BusinessError("导入数据缺少 meta.code")
        if self.__quiz_repo.get_by_code(code=code):
            raise BusinessError(f"测验编码 {code} 已存在")

        cp = meta.get("cover_prompt")
        quiz_model = QuizModel(
            name=meta.get("name", ""),
            code=code,
            quiz_type=meta.get("quiz_type", "vector"),
            status="draft",
            source="ai",
            share_title=meta.get("share_title"),
            share_desc=meta.get("share_desc"),
            fallback_outcome_code=meta.get("fallback_outcome_code"),
            cover_prompt={"prompt": cp} if isinstance(cp, str) else cp,
            algo_config=definition.get("algo_config"),
            special_rules=definition.get("special_rules"),
            result_config=meta.get("result_config"),
        )
        self.__quiz_repo.insert(model=quiz_model)

        quiz = self.__quiz_repo.get_by_code(code=code)

        for q in definition.get("questions", []):
            ip = q.get("image_prompt")
            question_model = QuizQuestionModel(
                quiz_id=quiz.id,
                seq=q.get("seq"),
                content=q.get("content", ""),
                image_prompt={"prompt": ip} if isinstance(ip, str) else ip,
                is_hidden=q.get("is_hidden", False),
                options=q.get("options", []),
                branch_config=q.get("branch_config"),
            )
            self.__question_repo.insert(model=question_model)

        for o in definition.get("outcomes", []):
            ap = o.get("avatar_prompt")
            outcome_model = QuizOutcomeModel(
                quiz_id=quiz.id,
                code=o.get("code"),
                name=o.get("name", ""),
                avatar_prompt={"prompt": ap} if isinstance(ap, str) else ap,
                summary=o.get("summary"),
                detail=o.get("detail"),
                tags=o.get("tags"),
                is_fallback=o.get("is_fallback", False),
                is_special=o.get("is_special", False),
                match_config=o.get("match_config"),
            )
            self.__outcome_repo.insert(model=outcome_model)

        return quiz.id
