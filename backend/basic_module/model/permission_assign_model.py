from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class EnumPermissionAssignGrantType(Enum):
    MENU = "MENU"
    BACKEND_API = "BACKEND_API"

    def __str__(self):
        labels = {
            EnumPermissionAssignGrantType.MENU: "菜单节点",
            EnumPermissionAssignGrantType.BACKEND_API: "后端接口",
        }
        return labels[self]


class EnumPermissionAssignGranteeType(Enum):
    ROLE = "ROLE"
    USER = "USER"
    WECOM_USER = "WECOM_USER"

    def __str__(self):
        labels = {
            EnumPermissionAssignGranteeType.ROLE: "角色",
            EnumPermissionAssignGranteeType.USER: "用户",
            EnumPermissionAssignGranteeType.WECOM_USER: "企业微信用户",
        }
        return labels[self]


class EnumPermissionAssignPolicy(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

    def __str__(self):
        labels = {
            EnumPermissionAssignPolicy.ALLOW: "允许",
            EnumPermissionAssignPolicy.DENY: "拒绝",
        }
        return labels[self]


class PermissionAssignModel(BasicVersionModel):
    grant_type: EnumPermissionAssignGrantType = Field(..., description="授权类型")
    grant_object_id: str = Field(..., description="授权对象ID")
    grantee_type: EnumPermissionAssignGranteeType = Field(..., description="被授权对象类型")
    grantee_object_id: str = Field(..., description="被授权对象ID")
    permission_id: Optional[str] = Field(None, description="权限ID")
    start_time: datetime = Field(..., description="授权开始时间")
    policy: Optional[EnumPermissionAssignPolicy] = Field(None, description="授权策略")
    end_time: Optional[datetime] = Field(None, description="授权结束时间")


class PermissionAssignViewModel(BasicVersionModel):
    grant_type: EnumPermissionAssignGrantType = Field(..., description="授权类型")
    grant_object_id: str = Field(..., description="授权对象ID")
    grant_object_name: Optional[str] = Field(None, description="授权对象名称")
    grantee_type: EnumPermissionAssignGranteeType = Field(..., description="被授权对象类型")
    grantee_object_id: str = Field(..., description="被授权对象ID")
    grantee_object_name: Optional[str] = Field(None, description="被授权对象名称")
    grantee_object_code: Optional[str] = Field(None, description="被授权对象编码")
    permission_id: str = Field(..., description="权限ID")
    start_time: datetime = Field(..., description="授权开始时间")
    policy: Optional[EnumPermissionAssignPolicy] = Field(None, description="授权策略")
    end_time: Optional[datetime] = Field(None, description="授权结束时间")
    ignore_auth: Optional[bool] = Field(None, description="是否忽略权限认证")
