from enum import Enum

from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class EnumFileResourceCategory(Enum):
    WECOM_USER = "WECOM_USER"

    def __str__(self):
        labels = {
            EnumFileResourceCategory.WECOM_USER: "企业微信用户",
        }
        return labels[self]


class EnumFileResourceRelationship(Enum):
    ANNEX = "ANNEX"
    AVATAR = "AVATAR"

    def __str__(self):
        labels = {
            EnumFileResourceRelationship.ANNEX: "附件",
            EnumFileResourceRelationship.AVATAR: "头像",
        }
        return labels[self]


class FileResourceModel(BasicVersionModel):
    file_info_id: str = Field(..., description="文件信息ID")
    resource_category: str = Field(..., description="资源类别")
    resource_id: str = Field(..., description="资源ID")
    relationship: str = Field(..., description="资源关系")
