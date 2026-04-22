from fastapi import Depends, Query, HTTPException
from dependency_injector.wiring import inject, Provide

from basic.api_response.api_response import ApiResponse
from basic.error.base_error import BusinessError
from basic.repository.unit_of_work import UnitOfWork
from biz_module import BizModuleContainer
from biz_module.model.quiz_token_model import QuizTokenModel
from biz_module.service.quiz_token_service import QuizTokenService


@inject
def get_quiz_token(
        token: str = Query(..., description="测验访问令牌"),
        uow: UnitOfWork = Depends(Provide[BizModuleContainer.unit_of_work]),
        quiz_token_service: QuizTokenService = Depends(Provide[BizModuleContainer.quiz_token_service]),
) -> QuizTokenModel:
    """仅校验 token 存在，不校验次数（供入口页使用）"""
    try:
        with uow:
            return quiz_token_service.get_detail(token=token)
    except BusinessError as e:
        raise HTTPException(status_code=403, detail=ApiResponse(code=40301, message=str(e)).to_json())


@inject
def validate_quiz_token(
        token: str = Query(..., description="测验访问令牌"),
        uow: UnitOfWork = Depends(Provide[BizModuleContainer.unit_of_work]),
        quiz_token_service: QuizTokenService = Depends(Provide[BizModuleContainer.quiz_token_service]),
) -> QuizTokenModel:
    """
    移动端专属依赖：校验 bt_quiz_token 中的 token 是否合法且有可用次数。
    通过 biz_module_container（已配置 DB）resolve quiz_token_service。
    """
    try:
        with uow:
            return quiz_token_service.validate_for_play(token=token)
    except BusinessError as e:
        raise HTTPException(status_code=403, detail=ApiResponse(code=40301, message=str(e)).to_json())
