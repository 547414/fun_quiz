from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel, BasicModel


class EnumRoleCode(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    WEB_USER = "WEB_USER"

    def __str__(self):
        labels = {
            EnumRoleCode.SUPER_ADMIN: "超级管理员",
            EnumRoleCode.ADMIN: "管理员",
            EnumRoleCode.WEB_USER: "普通用户",
        }
        return labels[self]


class EnumRoleScope(Enum):
    ADMIN = [EnumRoleCode.SUPER_ADMIN.value, EnumRoleCode.ADMIN.value]
    PEOPLE_MANAGE = [
        EnumRoleCode.SUPER_ADMIN.value,
        EnumRoleCode.ADMIN.value,
    ]

    def __str__(self):
        labels = {
            EnumRoleScope.ADMIN: "管理员",
            EnumRoleScope.PEOPLE_MANAGE: "人员管理",
        }
        return labels[self]


class RoleModel(BasicVersionModel):
    name: str = Field(..., description="角色名称")
    brief: Optional[str] = Field(None, description="描述")
    code: Optional[str] = Field(..., description="角色编码")
    enabled: bool = Field(..., description="是否启用")
    seq: int = Field(..., description="排序")


class EditRoleModel(RoleModel):
    seq: Optional[int] = Field(None, description="排序")

    def to_role_model(self) -> RoleModel:
        return RoleModel(
            id=self.id,
            name=self.name,
            brief=self.brief,
            code=self.code,
            enabled=self.enabled,
            seq=self.seq,
        )


class RolePageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段")


class ChangeRoleEnabledParamsModel(BasicModel):
    enabled: bool = Field(..., description="启用")


class RoleStatisticsModel(BasisModel):
    total: int = Field(..., description="总数")
    enabled_count: int = Field(..., description="启用总数")
    disable_count: int = Field(..., description="禁用总数")
    newest_updated_at: datetime = Field(..., description="最新更新时间")


class DeleteRoleParamsModel(BasisModel):
    role_id: str = Field(..., description="角色ID")


class RoleMaxSeqModel(BasicModel):
    max_seq: int = Field(..., description="最大排序值")
