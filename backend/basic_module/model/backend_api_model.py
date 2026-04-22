from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasicModel, BasisModel


class BackendApiModel(BasicVersionModel):
    name: Optional[str] = Field(None, description="名称")
    code: Optional[str] = Field(None, description="编码")
    enabled: bool = Field(..., description="启用")
    url: str = Field(..., description="url")
    ignore_auth: bool = Field(..., description="忽略验证")


class BackendApiViewModel(BasicModel):
    name: Optional[str] = Field(None, description="名称")
    code: Optional[str] = Field(None, description="编码")
    enabled: bool = Field(..., description="启用")
    url: str = Field(..., description="url")
    ignore_auth: bool = Field(..., description="忽略验证")


class BackendApiPageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段")


class ChangeBackendApiIgnoreAuthParamsModel(BasicModel):
    ignore_auth: bool = Field(..., description="忽略权限")
