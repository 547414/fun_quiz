from typing import Optional, Any, Dict

from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class ConfigDictModel(BasicVersionModel):
    name: Optional[str] = Field(None, description="名称")
    code: Optional[str] = Field(None, description="编码")
    data: Optional[Dict[str, Any]] = Field(None, description="数据")
    enabled: bool = Field(None, description="启用")
