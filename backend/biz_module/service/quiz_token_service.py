import secrets
import uuid
from typing import Optional, Set
from basic.error.base_error import BusinessError
from biz_module.model.quiz_token_model import (
    GenerateTokenParamsModel, TokenListParamsModel, QuizTokenModel, GeneratedTokensViewModel,
    UpdateTokenQuizIdsModel
)
from biz_module.repository.quiz_token_repository import QuizTokenRepository
from biz_module.repository.quiz_token_quiz_repository import QuizTokenQuizRepository


class QuizTokenService:
    def __init__(
        self,
        quiz_token_repository: QuizTokenRepository,
        quiz_token_quiz_repository: QuizTokenQuizRepository,
    ):
        self.__token_repo = quiz_token_repository
        self.__token_quiz_repo = quiz_token_quiz_repository

    def generate(self, params: GenerateTokenParamsModel) -> GeneratedTokensViewModel:
        batch_code = params.batch_code or f"batch_{secrets.token_hex(4)}"
        quiz_ids = params.quiz_ids if params.quiz_ids else []
        tokens = []

        for _ in range(params.count):
            token_str = secrets.token_urlsafe(32)
            token_model_id = str(uuid.uuid4())
            token_model = QuizTokenModel(
                id=token_model_id,
                token=token_str,
                status="active",
                max_uses=params.max_uses,
                used_count=0,
                source=params.source,
                batch_code=batch_code,
                expires_at=params.expires_at,
                extra=params.extra,
            )
            self.__token_repo.insert(model=token_model)
            if quiz_ids:
                self.__token_quiz_repo.insert_batch(token_id=token_model_id, quiz_ids=quiz_ids)
            tokens.append(token_str)

        return GeneratedTokensViewModel(
            tokens=tokens,
            batch_code=batch_code,
            count=len(tokens),
        )

    def page(self, params: TokenListParamsModel):
        return self.__token_repo.page(params=params)

    def get_detail(self, token: str):
        token_model = self.__token_repo.get_by_token(token=token)
        if not token_model:
            raise BusinessError("Token不存在")
        return token_model

    def validate_for_play(self, token: str) -> QuizTokenModel:
        """验证token是否可使用，返回token模型"""
        token_model = self.__token_repo.get_by_token(token=token)
        if not token_model:
            raise BusinessError("无效的访问链接")
        if token_model.status == "expired":
            raise BusinessError("访问链接已过期")
        if token_model.status == "exhausted":
            raise BusinessError("访问次数已用完")
        return token_model

    def get_allowed_quiz_ids(self, token_id: str) -> Optional[Set[str]]:
        """返回该 token 授权的测验 ID 集合，None 表示不限制"""
        return self.__token_quiz_repo.get_quiz_ids_by_token(token_id=token_id)

    def update_quiz_ids(self, params: UpdateTokenQuizIdsModel):
        token_model = self.__token_repo.get_by_id(token_id=params.token_id)
        if not token_model:
            raise BusinessError("Token不存在")
        self.__token_quiz_repo.delete_by_token_id(token_id=params.token_id)
        if params.quiz_ids:
            self.__token_quiz_repo.insert_batch(token_id=params.token_id, quiz_ids=params.quiz_ids)

    def mark_used(self, token_id: str):
        """完成一次答题后递增 used_count，次数耗尽时更新状态为 exhausted"""
        token_model = self.__token_repo.get_by_id(token_id=token_id)
        if not token_model:
            raise BusinessError("Token不存在")
        token_model.used_count = (token_model.used_count or 0) + 1
        if token_model.max_uses is not None and token_model.used_count >= token_model.max_uses:
            token_model.status = "exhausted"
        self.__token_repo.update(model=token_model)
