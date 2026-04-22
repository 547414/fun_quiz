from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel


class FileInfoModel(BasicVersionModel):
    name: str = Field(..., description="文件名称")
    file_storage_id: str = Field(..., description="文件存储ID")


class FileInfoViewModel(BasisModel):
    file_info_id: str = Field(..., description="文件信息ID")
    bucket_name: str = Field(..., description="存储桶名称")
    object_name: str = Field(..., description="对象名称")
    file_object_name: str = Field(..., description="文件对象名称")
    url: Optional[str] = Field(None, description="url")
    file_name: Optional[str] = Field(None, description="文件名称")
    file_size: Optional[int] = Field(None, description="文件大小")
    file_type: Optional[str] = Field(None, description="文件类型")


class FileInfoListParams(BasisModel):
    file_info_id_list: List[str] = Field(..., description="文件信息ID列表")
