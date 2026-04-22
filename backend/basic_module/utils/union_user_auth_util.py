import os

import toml
from fastapi import Depends, HTTPException, Request
from dependency_injector.wiring import inject, Provide

from basic.api_response.api_response import ApiResponse
from basic.repository.unit_of_work import UnitOfWork
from basic_module import BasicModuleContainer
from basic_module.model.union_user_user_model import EnumUnionUserCategory
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.union_user_service import UnionUserService

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.join(PATH, "../")
APP_CONFIG = toml.load(fr"{BASE_PATH}app_config.toml")
ACTIVE = APP_CONFIG.get('settings', {}).get('active', 'development')
CONFIG_NAME = f'app_{ACTIVE}_config.toml'
CONFIG = toml.load(fr"{BASE_PATH}config/{CONFIG_NAME}")


@inject
def validate_token(
        request: Request,
        uow: UnitOfWork = Depends(Provide[BasicModuleContainer.unit_of_work]),
        union_user_service: UnionUserService = Depends(Provide[BasicModuleContainer.union_user_service])
):
    with uow:
        # ignore_auth = union_user_service.check_backend_api_ignore(
        #     url=request.url.path,
        # )
        # if ignore_auth:
        #     return

        token = request.headers.get("Authorization")
        scene = request.headers.get("Scene", "DEFAULT")
        space = request.headers.get("Space", "DEFAULT")
        if token is None or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail=ApiResponse(code=40131, message="令牌缺失").to_json())

        token_value = token.split(" ")[1]

        return union_user_service.validate_token(
            token=token_value,
            url=request.url.path,
            space=space,
            scene=scene,
        )


def get_current_role_code(
        current_user_info: ValidateTokenResModel
):
    for user in current_user_info.union_user_info.user_list:
        if user.union_user_user_category == EnumUnionUserCategory.WEB_USER.value:
            return user.current_role_code
    return None


def get_current_wecom_user(
        current_user_info: ValidateTokenResModel
):
    for user in current_user_info.union_user_info.user_list:
        if user.union_user_user_category == EnumUnionUserCategory.WECOM_USER.value:
            return user
    return None
