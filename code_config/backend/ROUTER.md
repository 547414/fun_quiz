# router 约定

参考：`backend/app/router/menu_router.py`

## 规则

- 文件名 `xxx_router.py`，放在 `app/router/`，自动注册为 `/api/xxx`
- `router = APIRouter()` + `logger = logging.getLogger('xxx')`
- 每个路由函数：`@router.post('/path')` / `@router.get('/path/{id}')` + `@inject`
- 标准参数：`request: Request`, 入参 model, `current_user_info`, `uow: UnitOfWork`, service
- 固定结构：`result = ApiResponse()` → `try: uow.init_log_data → with uow: 业务 → except → return JSONResponse`
- 返回列表/对象时调用 `.model_dump()`
- 文件下载用 `StreamingResponse`，非 `JSONResponse`
- 方法调用必须写明参数名，多参数时每个参数独占一行（包括单参数）

## 示例骨架

```python
import logging
import traceback
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.utils.union_user_auth_util import validate_token

router = APIRouter()
logger = logging.getLogger('xxx')

@router.post('/action')
@inject
def route_action(
        request: Request,
        params: XxxParams,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        xxx_service: XxxService = Depends(
            Provide[Container.biz_module_container.xxx_service]
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
            result.data = xxx_service.action(
                params=params
            )
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())
```
