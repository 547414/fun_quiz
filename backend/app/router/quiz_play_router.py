import logging
import traceback
from typing import Optional

from fastapi import APIRouter, Body, Depends, Request, Query
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from biz_module.model.quiz_result_model import SubmitAnswersParamsModel, QuizTokenBody
from biz_module.service.quiz_play_service import QuizPlayService

router = APIRouter()
logger = logging.getLogger('quiz-play-router')


def _resolve_token(body_token: Optional[str], query_token: Optional[str]) -> Optional[str]:
    return body_token or query_token


@router.post('/entry')
@inject
def route_play_entry(
        request: Request,
        body: Optional[QuizTokenBody] = Body(None),
        token: Optional[str] = Query(None),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_play_service: QuizPlayService = Depends(
            Provide[Container.biz_module_container.quiz_play_service]
        ),
):
    result = ApiResponse()
    try:
        effective_token = _resolve_token(body_token=body.token if body else None, query_token=token)
        uow.init_log_data(
            current_user_info={},
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={},
        )
        with uow:
            data = quiz_play_service.get_entry(token=effective_token)
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/entry/quizzes')
@inject
def route_entry_quizzes(
        request: Request,
        body: Optional[QuizTokenBody] = Body(None),
        token: Optional[str] = Query(None),
        search: str = Query('', description="搜索关键字"),
        page_index: int = Query(1, description="页码"),
        page_size: int = Query(20, description="每页数量"),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_play_service: QuizPlayService = Depends(
            Provide[Container.biz_module_container.quiz_play_service]
        ),
):
    result = ApiResponse()
    try:
        effective_token = _resolve_token(body_token=body.token if body else None, query_token=token)
        uow.init_log_data(
            current_user_info={},
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"search": search},
        )
        with uow:
            data = quiz_play_service.get_entry_quizzes(
                token=effective_token,
                search=search,
                page_index=page_index,
                page_size=page_size,
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/entry/history')
@inject
def route_entry_history(
        request: Request,
        body: Optional[QuizTokenBody] = Body(None),
        token: Optional[str] = Query(None),
        search: str = Query('', description="搜索关键字"),
        page_index: int = Query(1, description="页码"),
        page_size: int = Query(20, description="每页数量"),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_play_service: QuizPlayService = Depends(
            Provide[Container.biz_module_container.quiz_play_service]
        ),
):
    result = ApiResponse()
    try:
        effective_token = _resolve_token(body_token=body.token if body else None, query_token=token)
        uow.init_log_data(
            current_user_info={},
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"search": search},
        )
        with uow:
            data = quiz_play_service.get_entry_history(
                token=effective_token,
                search=search,
                page_index=page_index,
                page_size=page_size,
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/play')
@inject
def route_play_data(
        request: Request,
        body: Optional[QuizTokenBody] = Body(None),
        token: Optional[str] = Query(None),
        quiz_id: str = Query(..., description="测验ID"),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_play_service: QuizPlayService = Depends(
            Provide[Container.biz_module_container.quiz_play_service]
        ),
):
    result = ApiResponse()
    try:
        effective_token = _resolve_token(body_token=body.token if body else None, query_token=token)
        uow.init_log_data(
            current_user_info={},
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"quiz_id": quiz_id},
        )
        with uow:
            data = quiz_play_service.get_play_data(
                token=effective_token,
                quiz_id=quiz_id,
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/submit')
@inject
def route_play_submit(
        request: Request,
        params: SubmitAnswersParamsModel,
        token: Optional[str] = Query(None),
        quiz_id: str = Query(..., description="测验ID"),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_play_service: QuizPlayService = Depends(
            Provide[Container.biz_module_container.quiz_play_service]
        ),
):
    result = ApiResponse()
    try:
        effective_token = _resolve_token(body_token=params.token, query_token=token)
        uow.init_log_data(
            current_user_info={},
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"quiz_id": quiz_id},
        )
        with uow:
            data = quiz_play_service.submit(
                token=effective_token,
                quiz_id=quiz_id,
                params=params,
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/result')
@inject
def route_play_result(
        request: Request,
        body: Optional[QuizTokenBody] = Body(None),
        token: Optional[str] = Query(None),
        result_id: str = Query(..., description="结果ID"),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_play_service: QuizPlayService = Depends(
            Provide[Container.biz_module_container.quiz_play_service]
        ),
):
    result = ApiResponse()
    try:
        effective_token = _resolve_token(body_token=body.token if body else None, query_token=token)
        uow.init_log_data(
            current_user_info={},
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"result_id": result_id},
        )
        with uow:
            data = quiz_play_service.get_result(
                token=effective_token,
                result_id=result_id,
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())
