from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field
import inflection


def camel_to_snake(obj: Any):
    """
    驼峰命名转下划线命名
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        data = {inflection.underscore(key): camel_to_snake(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        data = [camel_to_snake(item) for item in obj]
    else:
        data = obj
    return data


def snake_to_camel(obj: Any):
    """
    下划线命名转驼峰命名
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        data = {inflection.camelize(key, False): snake_to_camel(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        data = [snake_to_camel(item) for item in obj]
    else:
        data = obj
    return data


class BasisModel(BaseModel):
    convert_names: bool = Field(True, title="Convert Names", description="是否转换字段名")

    def __init__(self, **data):
        super().__init__(**camel_to_snake(data))

    def model_dump(self, *args, **kwargs):
        convert_names = self.convert_names
        data = self._convert_model_to_dict(self)
        if convert_names:
            return snake_to_camel(data)
        return data

    def _convert_model_to_dict(self, obj):
        if isinstance(obj, BaseModel):
            data_dict = {}
            for field_name in obj.model_fields:
                if field_name != "convert_names":
                    field_value = getattr(obj, field_name)
                    data_dict[field_name] = self._convert_model_to_dict(field_value)
            return data_dict
        elif isinstance(obj, list):
            return [self._convert_model_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            data_dict = {}
            for key, value in obj.items():
                if key != "convert_names":
                    data_dict[key] = self._convert_model_to_dict(value)
            return data_dict
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj


class BasicModel(BasisModel):
    id: Optional[str] = Field(None, title="ID", description="ID")


class BasicVersionModel(BasicModel):
    created_at: Optional[datetime] = Field(None, title="Created At", description="Created At")
    updated_at: Optional[datetime] = Field(None, title="Updated At", description="Updated At")
    operator: Optional[str] = Field(None, title="Operator", description="Operator")
    operator_category: Optional[str] = Field(None, title="Operator_Category", description="Operator_Category")
    desc: Optional[str] = Field(None, title="Desc", description="Desc")
    version: Optional[int] = Field(None, title="Version", description="Version")


class EnumOperatorCategory(Enum):
    ROBOT = "ROBOT"
    WEB_USER = "WEB_USER"
    UNION_USER = "UNION_USER"

    def __str__(self):
        labels = {
            EnumOperatorCategory.ROBOT: "机器人",
            EnumOperatorCategory.WEB_USER: "web用户",
            EnumOperatorCategory.UNION_USER: "联合用户",
        }
        return labels[self]
