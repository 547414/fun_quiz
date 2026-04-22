import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.invite_code_model import InviteCodePageParamsModel, EditInviteCodeParamsModel, \
    SoftDeleteInviteCodeParamsModel, ChangeInviteCodeEnableParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.invite_code_service import InviteCodeService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('invite_code')


@router.post('/page')
@inject
def route_get_invite_code_page(
        params: InviteCodePageParamsModel,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        invite_code_service: InviteCodeService = Depends(
            Provide[Container.basic_module_container.invite_code_service]
        )
):
    result = ApiResponse()

    try:
        with uow:
            page = invite_code_service.get_invite_code_page(
                params=params
            )
            result.data = page.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.get('/detail/{invite_code_id}')
@inject
def route_get_invite_code_detail(
        invite_code_id: str,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        invite_code_service: InviteCodeService = Depends(
            Provide[Container.basic_module_container.invite_code_service]
        )
):
    result = ApiResponse()

    try:
        with uow:
            data = invite_code_service.get_invite_code_detail(
                invite_code_id=invite_code_id
            )
            result.data = data.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_edit_invite_code(
        request: Request,
        params: EditInviteCodeParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        invite_code_service: InviteCodeService = Depends(
            Provide[Container.basic_module_container.invite_code_service]
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
            invite_code_service.edit(
                params=params,
                current_user_info=current_user_info
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/soft_delete')
@inject
def route_soft_delete_invite_code(
        request: Request,
        params: SoftDeleteInviteCodeParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        invite_code_service: InviteCodeService = Depends(
            Provide[Container.basic_module_container.invite_code_service]
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
            invite_code_service.soft_delete(
                params=params,
                current_user_info=current_user_info
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/change_enabled')
@inject
def route_change_invite_code_enabled(
        request: Request,
        params: ChangeInviteCodeEnableParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        invite_code_service: InviteCodeService = Depends(
            Provide[Container.basic_module_container.invite_code_service]
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
            invite_code_service.change_enabled(
                params=params,
                current_user_info=current_user_info
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.get('/statistics')
@inject
def route_get_invite_code_statistics(
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        invite_code_service: InviteCodeService = Depends(
            Provide[Container.basic_module_container.invite_code_service]
        )
):
    result = ApiResponse()

    try:
        with uow:
            data = invite_code_service.statistics()
            result.data = data.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
