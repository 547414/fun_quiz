# model 约定

参考：`backend/basic_module/model/menu_model.py`

## 规则

- **XxxModel**（继承 `BasicVersionModel`）：字段必须与 entity 列完全对应，不得包含非 DB 字段；insert/update 始终使用此类
- **XxxViewModel**（继承 `BasicModel` 或 `XxxModel`）：附加展示字段（如关联表名称），由 repository 中独立方法配合 JOIN SQL 返回
- **XxxEditModel**（继承 `XxxModel`）：编辑场景专用，可放宽字段约束（如 Optional），提供 `to_xxx_model()` 转换方法
- **XxxParamsModel**（继承 `BasisModel`）：请求入参，不对应 DB 表
- 所有字段使用 `Field(..., description="描述")` 或 `Field(默认值, description="描述")`
- `list` 用 `List`，`dict` 用 `Dict`

## 示例骨架

```python
from typing import Optional, List
from pydantic import Field
from basic.model.basic_model import BasicVersionModel, BasicModel, BasisModel

class XxxModel(BasicVersionModel):
    name: str = Field(..., description="名称")
    parent_id: Optional[str] = Field(None, description="父级ID")

class XxxViewModel(BasicModel):
    name: str = Field(..., description="名称")
    parent_name: Optional[str] = Field(None, description="父级名称")

class XxxPageParams(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
```
