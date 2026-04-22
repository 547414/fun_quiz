import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.menu_model import EditMenuModel, SaveMenuSeqAndParentModel, MenuTreeParamsModel, \
    MenuPageParamsModel, DeleteMenuParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.menu_service import MenuService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('menu')


@router.post('/tree', dependencies=[Depends(validate_token)])
@inject
def route_get_menu_tree(
        request: Request,
        params: MenuTreeParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
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
            menu_tree = menu_service.get_menu_tree(
                params=params,
            )
            result.data = [menu.model_dump() for menu in menu_tree]

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/allow_menu_tree')
@inject
def route_get_allow_menu_tree(
        request: Request,
        params: MenuTreeParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
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
            menu_tree = menu_service.get_allow_menu_tree(
                params=params,
                current_user_info=current_user_info
            )
            result.data = [menu.model_dump() for menu in menu_tree]

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/page')
@inject
def route_get_backend_api_page(
        request: Request,
        params: MenuPageParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
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
            menu_page = menu_service.get_menu_page(
                params=params
            )
            result.data = menu_page.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_edit_menu(
        request: Request,
        params: EditMenuModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
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
            menu_service.edit_menu(
                params=params,
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.get('/detail/{menu_id}')
@inject
def route_get_menu_detail(
        request: Request,
        menu_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={'menu_id': menu_id},
        )
        with uow:
            menu_detail = menu_service.get_menu_detail(
                menu_id=menu_id,
            )
            result.data = menu_detail.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/delete')
@inject
def route_delete_menu(
        request: Request,
        params: DeleteMenuParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
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
            menu_service.delete_menu(
                params=params,
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/save_seq_and_parent')
@inject
def route_save_seq_and_parent(
        request: Request,
        params: SaveMenuSeqAndParentModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        menu_service: MenuService = Depends(
            Provide[Container.basic_module_container.menu_service]
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
            menu_service.save_seq_and_parent(
                params=params,
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
