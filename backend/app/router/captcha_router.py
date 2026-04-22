import logging
import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic_module.model.captcha_model import CaptchaValidateParamsModel
from basic_module.service.captcha_service import CaptchaService

router = APIRouter()
logger = logging.getLogger('captcha')


@router.post('/generate')
@inject
def route_generate_captcha(
        captcha_service: CaptchaService = Depends(
            Provide[Container.basic_module_container.captcha_service]
        )
):
    result = ApiResponse()

    try:
        data = captcha_service.generate_verification_code_base64()
        result.data = result.data = data.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())


@router.post('/validate')
@inject
def route_validate_captcha(
        params: CaptchaValidateParamsModel,
        captcha_service: CaptchaService = Depends(
            Provide[Container.basic_module_container.captcha_service]
        )
):
    result = ApiResponse()

    try:
        validate_auth_code = captcha_service.validate_captcha(
            params=params
        )
        result.data = validate_auth_code

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))

    return JSONResponse(content=result.to_json())
