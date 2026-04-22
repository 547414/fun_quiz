# app/utils/auth_middleware.py

from typing import Union
from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Request, status, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.repository.unit_of_work import UnitOfWork
from basic_module.service.auth_service import AuthService


class AuthMiddleware(BaseHTTPMiddleware):
    @inject
    async def dispatch(
            self,
            request: Request,
            call_next,
            uow: UnitOfWork = Depends(
                Provide[Container.biz_module_container.unit_of_work]
            ),
            auth_service: AuthService = Depends(Provide[Container.basic_module_container.auth_service]),
    ):
        user_id = request.headers.get("userId")
        with uow:
            validate_pass = auth_service.validate_user_id(_user_id=user_id)
        if not user_id or not validate_pass:
            result = ApiResponse()
            result.code = 401
            result.message = "Unauthorized"
            return JSONResponse(content=result.to_json())

        response = await call_next(request)
        return response
