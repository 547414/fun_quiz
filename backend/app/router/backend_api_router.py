import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.backend_api_model import BackendApiPageParamsModel, ChangeBackendApiIgnoreAuthParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.backend_api_service import BackendApiService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('backend_api')


@router.post('/page')
@inject
def route_get_backend_api_page(
        request: Request,
        params: BackendApiPageParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        backend_api_service: BackendApiService = Depends(
            Provide[Container.basic_module_container.backend_api_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            backend_api_page = backend_api_service.get_backend_api_page(
                params=params
            )
            result.data = backend_api_page.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/change_ignore_auth')
@inject
def route_change_backend_api_ignore_auth(
        request: Request,
        params: ChangeBackendApiIgnoreAuthParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        backend_api_service: BackendApiService = Depends(
            Provide[Container.basic_module_container.backend_api_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            backend_api_service.change_backend_api_ignore_auth(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
