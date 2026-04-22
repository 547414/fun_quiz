from enum import Enum
from typing import Optional, List
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicVersionModel
from basic.model.tree_model import TreeModel


class EnumDeptCategory(Enum):
    COMPANY = 'COMPANY'
    DEPARTMENT = 'DEPARTMENT'
    OTHER = 'OTHER'

    def __str__(self):
        labels = {
            EnumDeptCategory.COMPANY: "公司",
            EnumDeptCategory.DEPARTMENT: "部门",
            EnumDeptCategory.OTHER: "其它",
        }
        return labels[self]


class EnumDeptSourceCategory(Enum):
    WECOM_DEPT = 'WECOM_DEPT'

    def __str__(self):
        labels = {
            EnumDeptSourceCategory.WECOM_DEPT: "企业微信部门",
        }
        return labels[self]


class DeptTreeParamsModel(BasisModel):
    organization_id: Optional[str] = Field(None, description="组织ID")
    level: Optional[int] = Field(None, description="层级")
    parent_id: Optional[str] = Field(None, description="父ID")
    search_value: Optional[str] = Field(None, description="搜索值")


class DeptModel(BasicVersionModel):
    organization_id: Optional[str] = Field(None, description="组织ID")
    name: str = Field(..., description="名称")
    code: str = Field(..., description="编码")
    category: Optional[str] = Field(None, description="类别")
    brief: Optional[str] = Field(None, description="描述")
    parent_id: Optional[str] = Field(None, description="父ID")
    source_category: Optional[str] = Field(None, description="来源类型，例如企微、钉钉等")
    source_id: Optional[str] = Field(None, description="来源id")
    seq: int = Field(0, description="排序序号")
    enabled: bool = Field(True, description="是否启用")


class DeptViewModel(DeptModel):
    name_list: Optional[List[str]] = Field(None, description="名称（路径）列表")

    def to_dept_model(self) -> DeptModel:
        return DeptModel(
            id=self.id,
            version=self.version,
            operator_category=self.operator_category,
            operator=self.operator_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            organization_id=self.organization_id,
            name=self.name,
            code=self.code,
            category=self.category,
            brief=self.brief,
            parent_id=self.parent_id,
            source_category=self.source_category,
            source_id=self.source_id,
            seq=self.seq,
            enabled=self.enabled
        )


class EditDeptParamsModel(DeptModel):
    seq: Optional[int] = Field(0, description="排序序号")
    enabled: Optional[bool] = Field(True, description="是否启用")

    def to_dept_model(self) -> DeptModel:
        return DeptModel(
            id=self.id,
            version=self.version,
            operator_category=self.operator_category,
            operator=self.operator,
            created_at=self.created_at,
            updated_at=self.updated_at,
            organization_id=self.organization_id,
            name=self.name,
            code=self.code,
            category=self.category,
            brief=self.brief,
            parent_id=self.parent_id,
            source_category=self.source_category,
            source_id=self.source_id,
            seq=self.seq,
            enabled=self.enabled
        )


class DeleteDeptParamsModel(BasisModel):
    dept_id: str = Field(..., description="部门ID")


class ChangeDeptEnabledParamsModel(BasisModel):
    dept_id: str = Field(..., description="部门ID")
    enabled: bool = Field(..., description="是否启用")


class DeptTreeViewModel(TreeModel):
    organization_id: Optional[str] = Field(None, description="组织ID")
    name: str = Field(..., description="名称")
    code: Optional[str] = Field(None, description="编码")
    category: Optional[str] = Field(None, description="类型")
    brief: Optional[str] = Field(None, description="描述")
    source_category: Optional[str] = Field(None, description="来源类型，例如企微、钉钉等")
    source_id: Optional[str] = Field(None, description="来源id")
    enabled: bool = Field(..., description="是否启用")
    children: Optional[List["DeptTreeViewModel"]] = Field(None, description="子列表")
    name_list: Optional[List[str]] = Field(None, description="名称（路径）列表")
    dept_id_list: Optional[List[str]] = Field(None, description="ID（路径）列表")
    has_child: Optional[bool] = Field(False, description="是否有子部门")
    seq_list: Optional[List[int]] = Field(None, description="排序序号列表")
    is_matched: Optional[bool] = Field(False, description="是否匹配")
    has_matched_children: Optional[bool] = Field(False, description="是否有匹配的子部门")

    def __post_init__(self):
        if self.children is None:
            self.children = []


class SaveDeptSeqAndParentModel(BasisModel):
    dept_tree: Optional[List[DeptTreeViewModel]] = Field(None, description="部门树")


class DeptMaxSeqModel(BasisModel):
    max_seq: int = Field(0, description="最大排序序号")
