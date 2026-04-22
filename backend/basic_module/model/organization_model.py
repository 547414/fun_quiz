from typing import Optional, List
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicVersionModel
from basic.model.tree_model import TreeModel


class OrganizationTreeParamsModel(BasisModel):
    level: Optional[int] = Field(None, description="层级")
    parent_id: Optional[str] = Field(None, description="父组织ID")
    search_value: Optional[str] = Field(None, description="搜索值")


class OrganizationModel(BasicVersionModel):
    name: str = Field(..., description="组织名称")
    code: str = Field(..., description="组织编码")
    category: Optional[str] = Field(None, description="组织类别")
    address: Optional[str] = Field(None, description="组织地址")
    parent_id: Optional[str] = Field(None, description="父组织ID")
    seq: int = Field(0, description="排序序号")
    enabled: bool = Field(True, description="是否启用")


class OrganizationViewModel(OrganizationModel):
    name_list: Optional[List[str]] = Field(None, description="组织名称（路径）列表")

    def to_organization_model(self) -> OrganizationModel:
        return OrganizationModel(
            id=self.id,
            version=self.version,
            operator_category=self.operator_category,
            operator=self.operator_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            code=self.code,
            category=self.category,
            address=self.address,
            parent_id=self.parent_id,
            seq=self.seq,
            enabled=self.enabled
        )


class EditOrganizationParamsModel(OrganizationModel):
    seq: Optional[int] = Field(0, description="排序序号")
    enabled: Optional[bool] = Field(True, description="是否启用")

    def to_organization_model(self) -> OrganizationModel:
        return OrganizationModel(
            id=self.id,
            version=self.version,
            operator_category=self.operator_category,
            operator=self.operator,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            code=self.code,
            category=self.category,
            address=self.address,
            parent_id=self.parent_id,
            seq=self.seq,
            enabled=self.enabled
        )


class DeleteOrganizationParamsModel(BasisModel):
    organization_id: str = Field(..., description="组织ID")


class ChangeOrganizationEnabledParamsModel(BasisModel):
    organization_id: str = Field(..., description="组织ID")
    enabled: bool = Field(..., description="是否启用")


class OrganizationTreeViewModel(TreeModel):
    name: str = Field(..., description="组织名称")
    code: Optional[str] = Field(None, description="组织编码")
    category: Optional[str] = Field(None, description="组织编码")
    address: Optional[str] = Field(None, description="组织编码")
    enabled: bool = Field(..., description="组织是否启用")
    children: Optional[List["OrganizationTreeViewModel"]] = Field(None, description="子组织列表")
    name_list: Optional[List[str]] = Field(None, description="组织名称（路径）列表")
    organization_id_list: Optional[List[str]] = Field(None, description="组织ID（路径）列表")
    has_child: Optional[bool] = Field(False, description="是否有子组织")
    seq_list: Optional[List[int]] = Field(None, description="排序序号列表")
    is_matched: Optional[bool] = Field(False, description="是否匹配")
    has_matched_children: Optional[bool] = Field(False, description="是否有匹配的子组织")

    def __post_init__(self):
        if self.children is None:
            self.children = []


class SaveOrganizationSeqAndParentModel(BasisModel):
    organization_tree: Optional[List[OrganizationTreeViewModel]] = Field(None, description="菜单树")
