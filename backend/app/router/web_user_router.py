import copy
import logging
import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.web_user_model import WebUserLoginParamsModel, AddWebUserModel, \
    EditWebUserModel, ResetWebUserPasswordModel, ResetWebUserSelfPasswordModel, UserRegisterParamsModel, \
    UserPageParamsModel, ChangeUserEnabledParamsModel, ChangeCurrentUserRoleParamsModel, UserListParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.web_user_service import WebUserService
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('user')


@router.post('/login')
@inject
def route_web_user_login(
        request: Request,
        user_login_params: WebUserLoginParamsModel,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=user_login_params.model_dump(),
        )
        with uow:
            scene = request.headers.get("Scene", None)
            space = request.headers.get("Space", None)
            user_info = user_service.user_login(
                params=user_login_params,
                scene=scene,
                space=space
            )
            if user_info:
                result.data = user_info.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/register')
@inject
def route_web_user_register(
        request: Request,
        params: UserRegisterParamsModel,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            user_service.register(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/add')
@inject
def route_add_user(
        request: Request,
        params: AddWebUserModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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
            user_service.add_user(
                params=params
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_edit_user(
        request: Request,
        params: EditWebUserModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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
            user_service.edit_user(
                params=params,
                current_user_info=current_user_info
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/page')
@inject
def route_get_user_page(
        request: Request,
        params: UserPageParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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
            user_page = user_service.get_user_page(
                params=params,
                current_user_info=current_user_info,
            )
            result.data = user_page.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/get_by_id_list')
@inject
def route_get_user_by_id_list(
        request: Request,
        params: UserListParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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

            user_list = user_service.get_by_id_list(
                params=params,
            )
            result.data = [user.model_dump() for user in user_list]

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/change_enabled')
@inject
def route_change_user_enabled(
        request: Request,
        params: ChangeUserEnabledParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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
            user_service.change_user_enabled(
                params=params,
                current_user_info=current_user_info
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.get('/detail/{user_id}')
@inject
def route_get_user_detail(
        request: Request,
        user_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
        )
):
    result = ApiResponse()

    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={
                'user_id': user_id
            },
        )
        with uow:
            user_detail = user_service.get_user_detail(
                user_id=user_id,
            )
            result.data = user_detail.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/reset_self_password')
@inject
def route_reset_password(
        request: Request,
        params: ResetWebUserSelfPasswordModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
        )
):
    result = ApiResponse()

    try:
        request_params_model = copy.deepcopy(params)
        request_params_model.old_password = '******'
        request_params_model.new_password = '******'
        request_params_model.new_password_repeat = '******'
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=request_params_model.model_dump(),
        )
        with uow:
            user_service.reset_self_password(
                params=params,
                current_user_info=current_user_info,
                space=request.headers.get("Space", "WEB")
            )

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/reset_password')
@inject
def route_reset_password(
        request: Request,
        params: ResetWebUserPasswordModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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
            new_password = user_service.reset_password(
                params=params,
                current_user_info=current_user_info
            )
            result.data = new_password

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/change_current_user_role')
@inject
def route_change_current_user_role(
        request: Request,
        params: ChangeCurrentUserRoleParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        user_service: WebUserService = Depends(
            Provide[Container.basic_module_container.web_user_service]
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
            scene = request.headers.get("Scene", None)
            space = request.headers.get("Space", None)
            res = user_service.change_current_user_role(
                params=params,
                current_user_info=current_user_info,
                scene=scene,
                space=space
            )
            result.data = res.model_dump()

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
