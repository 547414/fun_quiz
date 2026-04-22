from enum import Enum
from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasicModel, BasisModel
from basic.model.page_sort_model import EnumPageSortModel
from basic_module.model.permission_assign_model import PermissionAssignModel, PermissionAssignViewModel


class EnumResourcePermissionCategory(Enum):
    MENU = "MENU"
    BACKEND_API = "BACKEND_API"

    def __str__(self):
        labels = {
            EnumResourcePermissionCategory.MENU: "菜单节点",
            EnumResourcePermissionCategory.BACKEND_API: "后端接口",
        }
        return labels[self]


class PermissionModel(BasicVersionModel):
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限编码")
    resource_category: EnumResourcePermissionCategory = Field(..., description="资源类别")
    resource_id: str = Field(..., description="资源ID")
    enabled: Optional[bool] = Field(None, description="权限是否启用")


class PermissionViewModel(PermissionModel):
    assign_list: Optional[List[PermissionAssignViewModel]] = Field(None, description="授权列表")
    ignore_auth: Optional[bool] = Field(None, description="是否忽略权限认证")


class PermissionPageViewModel(BasicModel):
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限编码")
    resource_category: EnumResourcePermissionCategory = Field(..., description="资源类别")
    resource_id: str = Field(..., description="资源ID")
    resource_category_display: Optional[str] = Field(None, description="资源类别显示")
    enabled: Optional[bool] = Field(True, description="权限是否启用")
    assign_list: Optional[List[PermissionAssignViewModel]] = Field(None, description="授权列表")
    ignore_auth: Optional[bool] = Field(None, description="是否忽略权限认证")


class EditPermissionModel(BasicModel):
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限编码")
    resource_category: EnumResourcePermissionCategory = Field(..., description="资源类别")
    resource_id: Optional[str] = Field(None, description="资源ID")
    enabled: Optional[bool] = Field(True, description="权限是否启用")
    assign_list: Optional[List[PermissionAssignModel]] = Field(None, description="授权列表")

    def to_permission_model(self):
        return PermissionModel(
            name=self.name,
            code=self.code,
            resource_category=self.resource_category,
            resource_id=self.resource_id,
            enabled=self.enabled
        )


class ChangePermissionEnabledModel(BasicModel):
    enabled: bool = Field(..., description="启用状态")


class PermissionPageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    category_list: Optional[List[str]] = Field(None, description="类别列表")
    search: Optional[str] = Field(None, description="搜索关键字")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段")
    name_sort: Optional[EnumPageSortModel] = Field(None, description="名称排序")


class DeletePermissionParamsModel(BasisModel):
    permission_id: str = Field(..., description="权限ID")
