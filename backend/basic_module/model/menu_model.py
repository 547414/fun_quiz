from enum import Enum
from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasicModel, BasisModel
from basic.model.tree_model import TreeModel


class EnumMenuType(Enum):
    AGGREGATION = "AGGREGATION"
    NORMAL = "NORMAL"

    def __str__(self):
        labels = {
            EnumMenuType.AGGREGATION: "聚合菜单节点",
            EnumMenuType.NORMAL: "普通菜单节点",
        }
        return labels[self]


class MenuModel(BasicVersionModel):
    name: str = Field(..., description="菜单名称")
    code: str = Field(..., description="菜单编码")
    enabled: bool = Field(..., description="菜单是否启用")
    parent_id: Optional[str] = Field(None, description="父级菜单ID")
    url: Optional[str] = Field(None, description="菜单链接")
    icon: Optional[str] = Field(None, description="菜单图标")
    seq: int = Field(0, description="菜单排序")
    type: str = Field(..., description="菜单类型")


class MenuTreeViewModel(TreeModel):
    name: str = Field(..., description="菜单名称")
    code: str = Field(..., description="菜单编码")
    enabled: bool = Field(..., description="菜单是否启用")
    url: Optional[str] = Field(None, description="菜单链接")
    icon: Optional[str] = Field(None, description="菜单图标")
    label: Optional[str] = Field(None, description="菜单名称")
    path: Optional[str] = Field(None, description="菜单链接")
    type: EnumMenuType = Field(..., description="菜单类型")
    type_display: Optional[str] = Field(None, description="菜单类型显示")
    children: Optional[List["MenuTreeViewModel"]] = Field(None, description="子菜单列表")
    name_list: Optional[List[str]] = Field(None, description="菜单名称（路径）列表")

    def __post_init__(self):
        if self.children is None:
            self.children = []


class EditMenuModel(MenuModel):
    seq: Optional[int] = Field(0, description="菜单排序")

    def to_menu_model(self) -> MenuModel:
        return MenuModel(
            id=self.id,
            name=self.name,
            code=self.code,
            enabled=self.enabled,
            parent_id=self.parent_id,
            url=self.url,
            icon=self.icon,
            seq=self.seq,
            type=self.type,
            version=self.version
        )


class MenuViewModel(BasicModel):
    name: str = Field(..., description="菜单名称")
    code: str = Field(..., description="菜单编码")
    enabled: bool = Field(..., description="菜单是否启用")
    parent_id: Optional[str] = Field(None, description="父级菜单ID")
    url: Optional[str] = Field(None, description="菜单链接")
    icon: Optional[str] = Field(None, description="菜单图标")
    seq: int = Field(0, description="菜单排序")
    type: str = Field(..., description="菜单类型")
    name_list: Optional[List[str]] = Field(None, description="菜单名称（路径）列表")


class MenuMaxModel(BasisModel):
    max_seq: int = Field(0, description="最大排序值")


class SaveMenuSeqAndParentModel(BasisModel):
    menu_tree: Optional[List[MenuTreeViewModel]] = Field(None, description="菜单树")


class MenuTreeParamsModel(BasisModel):
    parent_id: Optional[str] = Field(None, description="父级菜单ID")


class DeleteMenuParamsModel(BasisModel):
    menu_id: str = Field(..., description="菜单ID")


class MenuPageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段")
