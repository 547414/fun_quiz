import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.utils.union_user_auth_util import validate_token
from biz_module.model.quiz_token_model import GenerateTokenParamsModel, TokenListParamsModel, UpdateTokenQuizIdsModel
from biz_module.service.quiz_token_service import QuizTokenService

router = APIRouter()
logger = logging.getLogger('quiz_token')


@router.post('/generate')
@inject
def route_token_generate(
        request: Request,
        params: GenerateTokenParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_token_service: QuizTokenService = Depends(
            Provide[Container.biz_module_container.quiz_token_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            data = quiz_token_service.generate(
                params=params
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/page')
@inject
def route_token_page(
        request: Request,
        params: TokenListParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_token_service: QuizTokenService = Depends(
            Provide[Container.biz_module_container.quiz_token_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            data = quiz_token_service.page(
                params=params
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/update_quiz_ids')
@inject
def route_token_update_quiz_ids(
        request: Request,
        params: UpdateTokenQuizIdsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_token_service: QuizTokenService = Depends(
            Provide[Container.biz_module_container.quiz_token_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            quiz_token_service.update_quiz_ids(params=params)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/detail/{token}')
@inject
def route_token_detail(
        request: Request,
        token: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_token_service: QuizTokenService = Depends(
            Provide[Container.biz_module_container.quiz_token_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"token": token},
        )
        with uow:
            data = quiz_token_service.get_detail(
                token=token
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())
