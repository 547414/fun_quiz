# enum 约定

参考：`backend/basic_module/model/menu_model.py` 中的 `EnumMenuType`

## 规则

- 枚举写在对应的 model 文件中，不单独建文件
- 继承 `Enum`，类名 `EnumXxxType`
- 值为大写字符串常量
- 必须实现 `__str__` 方法返回中文标签

## 示例

```python
from enum import Enum

class EnumXxxType(Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"

    def __str__(self):
        labels = {
            EnumXxxType.TYPE_A: "类型A",
            EnumXxxType.TYPE_B: "类型B",
        }
        return labels[self]
```
