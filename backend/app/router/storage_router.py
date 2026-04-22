import logging
import traceback

from fastapi import APIRouter, Depends, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.file_info_model import FileInfoListParams
from basic_module.model.upload_model import UploadBase64Params
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.storage_service import StorageService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('storage')


@router.post('/upload')
@inject
def route_upload(
        request: Request,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        file: UploadFile = File(...),
        filename: str = Form(None),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        storage_service: StorageService = Depends(
            Provide[Container.basic_module_container.storage_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
        )
        with uow:
            if filename:
                file_name = filename
            else:
                file_name = file.filename
            res = storage_service.upload(
                file=file.file,
                file_name=file_name
            )
            result.data = res.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/upload_base64')
@inject
def route_upload_base64(
        request: Request,
        params: UploadBase64Params,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        storage_service: StorageService = Depends(
            Provide[Container.basic_module_container.storage_service]
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
            res = storage_service.upload_base64(
                params=params
            )
            result.data = res.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/file_info_list')
@inject
def route_get_file_info_list(
        request: Request,
        params: FileInfoListParams,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        storage_service: StorageService = Depends(
            Provide[Container.basic_module_container.storage_service]
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
            res = storage_service.get_file_info_list(
                params=params,
            )
            result.data = [item.model_dump() for item in res]

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.get('/file_url/{file_info_id}')
@inject
def route_get_file_url(
        request: Request,
        file_info_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        storage_service: StorageService = Depends(
            Provide[Container.basic_module_container.storage_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={'file_info_id': file_info_id},
        )
        with uow:
            file_url = storage_service.get_file_url(
                file_info_id=file_info_id,
            )
            result.data = file_url

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
