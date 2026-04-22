import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.union_user_model import EditUnionUserInfoModel, UnionUserAuthCodeLoginParamsModel, \
    RefreshUnionUserAccessTokenModel, DeleteUnionUserModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.union_user_service import UnionUserService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('union_user')


@router.post('/edit_info')
@inject
def route_edit_union_user_info(
        request: Request,
        params: EditUnionUserInfoModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        union_user_service: UnionUserService = Depends(
            Provide[Container.basic_module_container.union_user_service]
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
            union_user_service.edit_union_user_info(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/auth_code_login')
@inject
def route_union_user_auth_code_login(
        request: Request,
        params: UnionUserAuthCodeLoginParamsModel,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        union_user_service: UnionUserService = Depends(
            Provide[Container.basic_module_container.union_user_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            scene = request.headers.get("Scene", None)
            space = request.headers.get("Space", None)
            data = union_user_service.auth_code_login(
                params=params,
                scene=scene,
                space=space,
            )
            result.data = data.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/refresh_access_token')
@inject
def route_refresh_token(
        request: Request,
        params: RefreshUnionUserAccessTokenModel,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        union_user_service: UnionUserService = Depends(
            Provide[Container.basic_module_container.union_user_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            scene = request.headers.get("Scene", None)
            space = request.headers.get("Space", None)
            res = union_user_service.refresh_access_token(
                refresh_token=params.refresh_token,
                space=space,
                scene=scene,
            )
            result.data = res.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/logout')
@inject
def route_logout(
        request: Request,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        union_user_service: UnionUserService = Depends(
            Provide[Container.basic_module_container.union_user_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            request_info=FastApiRequestForLogModel.init(request=request),
        )
        with uow:
            union_user_service.logout(
                current_user_info=current_user_info,
                space=request.headers.get("Space", "WEB")
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/delete')
@inject
def route_delete_union_user(
        request: Request,
        params: DeleteUnionUserModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        union_user_service: UnionUserService = Depends(
            Provide[Container.basic_module_container.union_user_service]
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
            union_user_service.delete(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
