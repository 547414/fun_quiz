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
from biz_module.model.quiz_model import (
    EditQuizParamsModel, DeleteQuizParamsModel, PublishQuizParamsModel,
    ImportQuizParamsModel, QuizListParamsModel
)
from biz_module.model.quiz_question_model import BatchSaveQuestionsParamsModel
from biz_module.model.quiz_outcome_model import BatchSaveOutcomesParamsModel
from biz_module.service.quiz_service import QuizService
from biz_module.service.quiz_stats_service import QuizStatsService

router = APIRouter()
logger = logging.getLogger('quiz')


@router.post('/page')
@inject
def route_quiz_page(
        request: Request,
        params: QuizListParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
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
            data = quiz_service.page(
                params=params
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_quiz_edit(
        request: Request,
        params: EditQuizParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
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
            quiz_service.edit(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/detail/{quiz_id}')
@inject
def route_quiz_detail(
        request: Request,
        quiz_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"quiz_id": quiz_id},
        )
        with uow:
            data = quiz_service.detail(
                quiz_id=quiz_id
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/delete')
@inject
def route_quiz_delete(
        request: Request,
        params: DeleteQuizParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
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
            quiz_service.delete(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/change_status')
@inject
def route_quiz_change_status(
        request: Request,
        params: PublishQuizParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
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
            quiz_service.change_status(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/import')
@inject
def route_quiz_import(
        request: Request,
        params: ImportQuizParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={},
        )
        with uow:
            quiz_id = quiz_service.import_from_definition(
                params=params
            )
            result.data = {"quiz_id": quiz_id}
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/questions/batch_save')
@inject
def route_quiz_batch_save_questions(
        request: Request,
        params: BatchSaveQuestionsParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
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
            quiz_service.batch_save_questions(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/questions/{quiz_id}')
@inject
def route_quiz_get_questions(
        request: Request,
        quiz_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"quiz_id": quiz_id},
        )
        with uow:
            data = quiz_service.get_questions(
                quiz_id=quiz_id
            )
            result.data = [item.model_dump() for item in data]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/outcomes/batch_save')
@inject
def route_quiz_batch_save_outcomes(
        request: Request,
        params: BatchSaveOutcomesParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
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
            quiz_service.batch_save_outcomes(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/outcomes/{quiz_id}')
@inject
def route_quiz_get_outcomes(
        request: Request,
        quiz_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_service: QuizService = Depends(
            Provide[Container.biz_module_container.quiz_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"quiz_id": quiz_id},
        )
        with uow:
            data = quiz_service.get_outcomes(
                quiz_id=quiz_id
            )
            result.data = [item.model_dump() for item in data]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/stats/{quiz_id}')
@inject
def route_quiz_stats(
        request: Request,
        quiz_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.biz_module_container.unit_of_work]),
        quiz_stats_service: QuizStatsService = Depends(
            Provide[Container.biz_module_container.quiz_stats_service]
        ),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={"quiz_id": quiz_id},
        )
        with uow:
            data = quiz_stats_service.get_stats(
                quiz_id=quiz_id
            )
            result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())
