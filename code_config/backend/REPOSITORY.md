# repository 约定

参考：`backend/basic_module/repository/menu_repository.py`

## 规则

- 继承 `BaseRepository`，构造函数接收 `session: Session` 并调用 `super().__init__(session)`
- **insert / update / delete_by_id** 为固定模板，不允许修改：
    - `insert` → `self.add(model=, entity=)`
    - `update` → `self.update_entity(entity=, entity_id=, model=)`
    - `delete_by_id` → `self.delete(entity=, entity_id=)`
- **禁止**直接使用 `self.session`，必须通过 `BaseRepository` 提供的方法操作数据
- 非必要不使用 `execute_sql`
- 查询方法使用 `get_by_params` / `get_all_by_params` / `get_page`，SQL 用三引号包裹，三引号后和结束三引号前必须换行；**拼接片段（`where +=` 等）也必须用三引号且同样换行**，如：
  ```python
  where += """
  AND name ILIKE :search
  """
  ```
- 方法调用必须写明参数名，多参数时每个参数独占一行（包括单参数）
- 返回 ViewModel 的查询写独立方法（如 `find_page` / `get_view_by_id`）

## 容器注册

在对应的 `xxx_module_container.py` 中用 `providers.Factory` 注册：
```python
xxx_repository = providers.Factory(
  XxxRepository
)
```

## 示例骨架

```python
from typing import Optional
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from xxx_module.entity.xxx import XxxEntity
from xxx_module.model.xxx_model import XxxModel, XxxViewModel


class XxxRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: XxxModel):
        return self.add(
            model=model,
            entity=XxxEntity
        )

    def update(self, model: XxxModel):
        return self.update_entity(
            entity=XxxEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=XxxEntity,
            entity_id=data_id
        )

    def get_by_id(self, data_id: str) -> Optional[XxxModel]:
        sql = """
        SELECT * FROM bt_xxx WHERE id = :data_id
        """

        return self.get_by_params(
            sql=sql,
            model=XxxModel,
            params={
                "data_id": data_id
            }
        )
```
