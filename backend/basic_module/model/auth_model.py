from enum import Enum
from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasisModel
from basic_module.model.union_user_model import UnionUserInfoModel


class EnumUserCategory(Enum):
    WEB_USER = "WEB_USER"
    WW = "WW"
    WX = "WX"
    UNION_USER = "UNION_USER"

    def __str__(self):
        labels = {
            EnumUserCategory.WEB_USER: "web用户",
            EnumUserCategory.WW: "企微用户",
            EnumUserCategory.WX: "微信用户",
            EnumUserCategory.UNION_USER: "联合用户"
        }
        return labels[self]


class JwtPayloadInfo(BasisModel):
    exp: Optional[int] = Field(None, description="过期时间")
    union_user_info: Optional[UnionUserInfoModel] = Field(None, description="联合用户信息")


class EnumSpace(Enum):
    WEB = "WEB"
    WECOM = "WECOM"

    def __str__(self):
        labels = {
            EnumSpace.WEB: "Web",
            EnumSpace.WECOM: "企微",
        }
        return labels[self]

    def __covert__(self):
        labels = {
            EnumSpace.WEB: "WEB_USER",
            EnumSpace.WECOM: "WECOM_USER",
        }
        return labels[self]
