from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasisModel


class UploadBase64Params(BasisModel):
    file: str = Field(..., description="Base64编码的文件内容")
    file_name: Optional[str] = Field(None, description="文件名称")
    file_size: Optional[int] = Field(None, description="文件大小")


class UploadResModel(BasisModel):
    file_info_id: Optional[str] = Field(None, description="文件信息ID")
    file_name: Optional[str] = Field(None, description="文件名称")
    file_type: Optional[str] = Field(None, description="文件类型")
    file_size: Optional[int] = Field(None, description="文件大小")
    bucket_name: Optional[str] = Field(None, description="存储桶名称")
    object_name: Optional[str] = Field(None, description="对象名称")
    file_object_name: Optional[str] = Field(None, description="文件对象名称")
    url: Optional[str] = Field(None, description="文件访问URL")
    file_hash: Optional[str] = Field(None, description="文件哈希值")
