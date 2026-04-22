# service 约定

参考：`backend/basic_module/service/menu_service.py`

## 规则

- 构造函数注入依赖（repository / 其他 service / minio_client 等），存为 `self.__xxx` 私有属性
- 不直接操作 session，通过 repository 完成数据库操作
- 方法调用必须写明参数名，多参数时每个参数独占一行（包括单参数）
- 入参/出参用 model 封装（BasisModel / XxxModel / XxxViewModel）
- 新增/更新逻辑：从 repository 取出 model → 修改字段 → 调用 repository.update

## 容器注册

在对应的 `xxx_module_container.py` 中用 `providers.Factory` 注册，显式传入依赖：

```python
xxx_service = providers.Factory(
    XxxService,
    xxx_repository=xxx_repository,
    minio_client=minio_client,
)
```

## 示例骨架

```python
from typing import Optional
from xxx_module.model.xxx_model import XxxModel, XxxSaveParams
from xxx_module.repository.xxx_repository import XxxRepository

class XxxService:
    def __init__(self, xxx_repository: XxxRepository):
        self.__xxx_repository = xxx_repository

    def save(self, params: XxxSaveParams) -> str:
        if params.id:
            model = self.__xxx_repository.get_by_id(
                data_id=params.id
            )
            model.name = params.name
            self.__xxx_repository.update(
                model=model
            )
        else:
            model = XxxModel(
                name=params.name
            )
            self.__xxx_repository.insert(
                model=model
            )
        return model.id

    def get_detail(self, data_id: str) -> Optional[XxxModel]:
        return self.__xxx_repository.get_by_id(
            data_id=data_id
        )
```
