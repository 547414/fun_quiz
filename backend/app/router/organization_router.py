import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.organization_model import OrganizationTreeParamsModel, EditOrganizationParamsModel, \
    DeleteOrganizationParamsModel, ChangeOrganizationEnabledParamsModel, SaveOrganizationSeqAndParentModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.organization_service import OrganizationService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('organization')


@router.post('/tree')
@inject
def route_organization_tree(
        request: Request,
        params: OrganizationTreeParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        organization_service: OrganizationService = Depends(
            Provide[Container.basic_module_container.organization_service]
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
            organization_page = organization_service.tree(
                params=params
            )
            result.data = [item.model_dump() for item in organization_page]

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_edit_organization(
        request: Request,
        params: EditOrganizationParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        organization_service: OrganizationService = Depends(
            Provide[Container.basic_module_container.organization_service]
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
            organization_service.edit(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.get('/detail/{organization_id}')
@inject
def route_get_organization_detail(
        request: Request,
        organization_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        organization_service: OrganizationService = Depends(
            Provide[Container.basic_module_container.organization_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={
                "organization_id": organization_id
            },
        )
        with uow:
            data = organization_service.detail(
                organization_id=organization_id
            )
            result.data = data.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/delete')
@inject
def route_delete_organization(
        request: Request,
        params: DeleteOrganizationParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        organization_service: OrganizationService = Depends(
            Provide[Container.basic_module_container.organization_service]
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
            organization_service.delete(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/change_enabled')
@inject
def route_change_organization_enabled(
        request: Request,
        params: ChangeOrganizationEnabledParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        organization_service: OrganizationService = Depends(
            Provide[Container.basic_module_container.organization_service]
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
            organization_service.change_enabled(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/save_seq_and_parent')
@inject
def route_save_organization_seq_and_parent(
        request: Request,
        params: SaveOrganizationSeqAndParentModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        organization_service: OrganizationService = Depends(
            Provide[Container.basic_module_container.organization_service]
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
            organization_service.save_seq_and_parent(
                params=params,
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
