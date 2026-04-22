from enum import Enum

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasicModel


class EnumUserRoleCategory(Enum):
    WEB_USER = "WEB_USER"
    WECOM_USER = "WECOM_USER"

    def __str__(self):
        labels = {
            EnumUserRoleCategory.WEB_USER: "用户",
            EnumUserRoleCategory.WECOM_USER: "企微用户"
        }
        return labels[self]


class UserRoleModel(BasicVersionModel):
    user_id: str = Field(..., description="用户id")
    user_category: EnumUserRoleCategory = Field(..., description="用户类型，企微用户、用户")
    role_id: str = Field(..., description="角色id")


class UserRoleViewModel(BasicVersionModel):
    user_id: str = Field(..., description="用户id")
    user_category: EnumUserRoleCategory = Field(..., description="用户类型，企微用户、用户")
    role_id: str = Field(..., description="角色id")
    role_code: str = Field(..., description="角色编码")


class SetWecomAdminParamsModel(BasicModel):
    wecom_user_uuid: str = Field(..., description="企微用户id")


class SetWecomDbParamsModel(BasicModel):
    wecom_user_uuid: str = Field(..., description="企微用户id")


class CancelWecomAdminParamsModel(BasicModel):
    wecom_user_uuid: str = Field(..., description="企微用户id")


class CancelWecomRoleParamsModel(BasicModel):
    wecom_user_uuid: str = Field(..., description="企微用户id")
