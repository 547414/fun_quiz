# entity 约定

参考：`backend/basic_module/entity/menu.py`

## 规则

- 继承 `BasicEntity`（自带 id/created_at/updated_at/operator/operator_category/version/desc）
- `__tablename__`：表名，格式 `ct_xxx`（核心）/ `bt_xxx`（业务）
- `__table_args__`：元组，包含 Index 和 `{"comment": "表注释"}`
- 字段用 `Column(Type, nullable=?, comment='注释')`，有默认值加 `server_default`
- 不写业务逻辑、不加 relationship

## 示例骨架

```python
from sqlalchemy import Column, String, Boolean, Integer, Index
from basic.entity.basic_entity import BasicEntity

class XxxEntity(BasicEntity):
    __tablename__ = 'bt_xxx'
    __table_args__ = (
        Index('idx_bt_xxx_field', 'field'),
        {"comment": "Xxx表"}
    )

    name = Column(String(500), nullable=False, comment='名称')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
```
